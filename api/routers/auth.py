import logging

from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pyseto import PysetoError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated

from api import schemes
from api.core.security import (
    create_access_token,
    decode_token,
    verify_password,
)
from api.crud.users import get_user_by_email

from api.database import get_db
from api.db.models import User

logger = logging.getLogger("irapi")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        405: {"description": "Method not Allowed"},
        422: {"description": "Unprocessable Entity"},
    },
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", scheme_name="OAuth2 Schema"
)


async def authenticate_user(
    email: str, password: str, db: Annotated[AsyncSession, Depends(get_db)]
) -> User | bool:
    logger.debug(f"Trying to authenticate {email}")
    user = await get_user_by_email(db=db, email=email)
    if not user:
        logger.warning(f"No user found with email: {email}")
        return False
    try:
        if verify_password(user.hashed_password, password):
            logger.debug(f"Verified password for user: {email}")
            return user
    except VerifyMismatchError as e:
        logger.warning(f"{e} for user: {email}")
    return False


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token).payload
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = schemes.TokenData(email=email)
    except PysetoError:
        raise credentials_exception
    user = await get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemes.User, Depends(get_current_user)],
) -> schemes.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/login", response_model=schemes.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# TODO: revoke, refresh token
