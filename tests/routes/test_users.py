import pytest

from datetime import datetime
from zoneinfo import ZoneInfo
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    # HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    # HTTP_403_FORBIDDEN,
    # HTTP_404_NOT_FOUND,
    # HTTP_405_METHOD_NOT_ALLOWED,
    # HTTP_422_UNPROCESSABLE_ENTITY
)

from api.core.security import create_access_token

TZ = ZoneInfo("Europe/Vienna")


@pytest.mark.anyio
async def test_read_users_unauthenticated(async_client) -> None:
    res = await async_client.get("/api/v1/users", follow_redirects=True)
    assert res.status_code == HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Not authenticated"}


@pytest.mark.anyio
async def test_create_new_user(async_client) -> None:
    dt_before = datetime.now(TZ)
    json_data = {"email": "testuser@test.test", "password": "test"}
    res = await async_client.post("/api/v1/users", json=json_data, follow_redirects=True)
    assert res.status_code == HTTP_201_CREATED
    res_json = res.json()
    # extract timestamps
    created_at = datetime.fromisoformat(res_json.pop("created_at"))
    modified_at = datetime.fromisoformat(res_json.pop("modified_at"))
    assert created_at == modified_at
    assert dt_before < created_at
    assert res_json == {"email": "testuser@test.test", "id": 1, "is_active": True}


@pytest.mark.anyio
async def test_read_users_authenticated(async_client) -> None:
    access_token = create_access_token(data={"email": "testuser@test.test"})  # bytestr
    res = await async_client.get(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {access_token.decode('utf-8')}",
        },
        follow_redirects=True,
    )
    assert res.status_code == HTTP_200_OK
    assert len(res.json()) == 1
    res_json = res.json()[0]
    del res_json["created_at"]
    del res_json["modified_at"]
    assert res_json == {"email": "testuser@test.test", "id": 1, "is_active": True}
