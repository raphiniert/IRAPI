import pytest

from datetime import datetime
from zoneinfo import ZoneInfo
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    # HTTP_401_UNAUTHORIZED,
    # HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    # HTTP_405_METHOD_NOT_ALLOWED,
    # HTTP_422_UNPROCESSABLE_ENTITY
)

TZ = ZoneInfo("Europe/Vienna")


@pytest.mark.anyio
async def test_read_devices(async_client) -> None:
    res = await async_client.get("/api/v1/devices", follow_redirects=True)
    assert res.status_code == HTTP_200_OK
    assert res.json() == []


@pytest.mark.anyio
async def test_create_new_device(async_client) -> None:
    dt_before = datetime.now(TZ)
    json_data = {"name": "New device", "signals": []}
    res = await async_client.post(
        "/api/v1/devices", json=json_data, follow_redirects=True
    )
    assert res.status_code == HTTP_201_CREATED
    res_json = res.json()
    # extract timestamps
    created_at = datetime.fromisoformat(res_json.pop("created_at"))
    modified_at = datetime.fromisoformat(res_json.pop("modified_at"))
    assert created_at == modified_at
    assert dt_before < created_at
    assert res_json == {
        "id": 1,
        "name": "New device",
        "signals": [],
    }


@pytest.mark.anyio
async def test_read_device(async_client) -> None:
    res = await async_client.get("/api/v1/devices/1", follow_redirects=True)
    assert res.status_code == HTTP_200_OK
    res_json = res.json()
    # ignore timestamps
    del res_json["created_at"]
    del res_json["modified_at"]
    assert res_json == {
        "id": 1,
        "name": "New device",
        "signals": [],
    }


@pytest.mark.anyio
async def test_patch_device(async_client) -> None:
    dt_before = datetime.now(TZ)
    json_data = {"id": 1, "name": "New altered device"}
    res = await async_client.patch(
        "/api/v1/devices/1", json=json_data, follow_redirects=True
    )
    assert res.status_code == HTTP_200_OK
    res_json = res.json()
    # extract timestamps
    created_at = datetime.fromisoformat(res_json.pop("created_at"))
    modified_at = datetime.fromisoformat(res_json.pop("modified_at"))
    assert created_at < dt_before < modified_at
    assert res_json == {
        "id": 1,
        "name": "New altered device",
        "signals": [],
    }


@pytest.mark.anyio
async def test_patch_mismatching_id_raises_error(async_client) -> None:
    json_data = {
        "id": 2,
        "name": "Wrong id device",
        "signals": [],
    }
    res = await async_client.patch(
        "/api/v1/devices/1", json=json_data, follow_redirects=True
    )
    assert res.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_remove_device(async_client) -> None:
    res = await async_client.request(
        method="DELETE", url="/api/v1/devices/1", follow_redirects=True
    )
    assert res.status_code == HTTP_200_OK
    assert res.json() == {"message": "IRDevice with id: 1 deleted"}


@pytest.mark.anyio
async def test_invalid_id_raises_error(async_client) -> None:
    res = await async_client.get("/api/v1/devices/1", follow_redirects=True)
    assert res.status_code == HTTP_404_NOT_FOUND
