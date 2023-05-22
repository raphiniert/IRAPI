import pytest

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    # HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    # HTTP_403_FORBIDDEN,
    # HTTP_404_NOT_FOUND,
    # HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from api.core.config import settings
from api.core.security import decode_token
from api.routers.auth import authenticate_user

TZ = ZoneInfo("Europe/Vienna")


@pytest.mark.anyio
async def test_create_new_user(async_client) -> None:
    json_data = {"email": "test@test.test", "password": "test"}
    res = await async_client.post("/api/v1/users", json=json_data, follow_redirects=True)
    assert res.status_code == HTTP_201_CREATED
    res_json = res.json()
    # extract timestamps
    del res_json["created_at"]
    del res_json["modified_at"]
    assert res_json == {"email": "test@test.test", "id": 1, "is_active": True}


@pytest.mark.anyio
async def test_authenticate_user_invalid_email(caplog, get_testing_session) -> None:
    async with get_testing_session as db:
        res = await authenticate_user(email="invalid@test.test", password="test", db=db)
        assert res is False
        assert [
            "Trying to authenticate invalid@test.test",
            "No user found with email: invalid@test.test",
        ] == [rec.message for rec in caplog.records]


@pytest.mark.anyio
async def test_authenticate_user_invalid_password(caplog, get_testing_session) -> None:
    async with get_testing_session as db:
        res = await authenticate_user(email="test@test.test", password="invalid", db=db)
        assert res is False
        assert [
            "Trying to authenticate test@test.test",
            "The password does not match the supplied hash for user: test@test.test",
        ] == [rec.message for rec in caplog.records]


@pytest.mark.anyio
async def test_authenticate_user_valid_password(caplog, get_testing_session) -> None:
    async with get_testing_session as db:
        res = await authenticate_user(email="test@test.test", password="test", db=db)
        assert res
        assert [
            "Trying to authenticate test@test.test",
            "Verified password for user: test@test.test",
        ] == [rec.message for rec in caplog.records]


@pytest.mark.anyio
async def test_login_for_access_token_invalid_data(async_client) -> None:
    res = await async_client.post(
        "/api/v1/auth/login",
        data={
            "grant_type": "password",
            "username": "invalid@test.test",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_login_for_access_token_invalid_mail(async_client) -> None:
    res = await async_client.post(
        "/api/v1/auth/login",
        data={
            "grant_type": "password",
            "username": "invalid@test.test",
            "password": "test",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Incorrect username or password"}


@pytest.mark.anyio
async def test_login_for_access_token_invalid_password(async_client) -> None:
    res = await async_client.post(
        "/api/v1/auth/login",
        data={
            "grant_type": "password",
            "username": "test@test.test",
            "password": "invalid",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Incorrect username or password"}


@pytest.mark.anyio
async def test_login_for_access_token(async_client) -> None:
    dt_before = datetime.now(TZ)
    res = await async_client.post(
        "/api/v1/auth/login",
        data={
            "grant_type": "password",
            "username": "test@test.test",
            "password": "test",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == HTTP_200_OK
    res_json = res.json()
    assert res_json["token_type"] == "bearer"

    # extract and decode access token
    access_token = res_json["access_token"]
    decoded_token = decode_token(access_token).payload
    assert decoded_token["email"] == "test@test.test"

    # verify dt_before + access_token_expire_seconds - 1 < token_expires_at < dt_before + access_token_expire_seconds + 1  # noqa: E501
    token_expires_at = datetime.fromisoformat(decoded_token["exp"])
    assert (
        dt_before + timedelta(seconds=settings.access_token_expire_seconds - 1)
        < token_expires_at
    )
    assert token_expires_at < dt_before + timedelta(
        seconds=settings.access_token_expire_seconds + 1
    )
