import uuid
from unittest import mock

from fastapi.testclient import TestClient

from jaanevis.api.fastapi.main import app
from jaanevis.config import settings
from jaanevis.domain.user import User, UserRead, UserUpdateApi
from jaanevis.responses import response as res

client = TestClient(app)
PREFIX = settings.API_V1_STR
user = User(
    email="a@example.com",
    username="username",
    password="password",
    is_active=True,
)


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.update_own_user.UpdateOwnUserUseCase")
def test_update_own_user(mock_usecase, auth_usecase) -> None:
    user_update = UserUpdateApi(username="username")
    updated_user_read = UserRead(username=user_update.username, is_active=True)
    mock_usecase().execute.return_value = res.ResponseSuccess(
        updated_user_read
    )
    session = uuid.uuid4()

    response = client.put(
        PREFIX + "/user/own",
        json=user_update.dict(),
        headers={"cookie": f"session={session}"},
    )
    result = response.json()

    assert result == updated_user_read
    assert response.status_code == 200
    mock_usecase().execute.assert_called()


def test_update_own_user_respose_unauthorized_with_no_cookie() -> None:
    user = UserUpdateApi(username="username")
    response = client.put(PREFIX + "/user/own", json=user.dict())

    assert response.status_code == 401


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.usecases.update_own_user.UpdateOwnUserUseCase")
def test_update_own_user_from_wrong_user(mock_usecase, auth_usecase) -> None:
    user_update = UserUpdateApi(username="username")
    mock_usecase().execute.return_value = (
        res.ResponseFailure.build_parameters_error("forbidden")
    )
    session = uuid.uuid4()

    response = client.put(
        PREFIX + "/user/own",
        json=user_update.dict(),
        headers={"cookie": f"session={session}"},
    )
    result = response.json()

    assert response.status_code == 403
    assert result == {"detail": "forbidden"}
