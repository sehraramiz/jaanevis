import uuid
from datetime import datetime, timedelta
from unittest import mock

from fastapi.testclient import TestClient

from jaanevis import requests as req
from jaanevis.api.fastapi.main import app
from jaanevis.config import settings
from jaanevis.responses import response as res

PREFIX = settings.API_V1_STR
client = TestClient(app)


@mock.patch("jaanevis.requests.login_request.LoginRequest")
@mock.patch("jaanevis.usecases.login.LoginUseCase")
def test_login(mock_usecase, request_mock) -> None:
    body = {"username": "username", "password": "password"}
    tomorrow = datetime.now() + timedelta(days=1)
    expire_tomorrow = tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT")
    mock_usecase().execute.return_value = res.ResponseSuccess(
        {"session": "validsession", "expires": expire_tomorrow}
    )

    response = client.post(PREFIX + "/user/login", json=body)

    assert response.status_code == 200
    mock_usecase().execute.assert_called()
    request_mock.build.assert_called_with(
        username="username", password="password"
    )
    assert "set-cookie" in dict(response.headers)
    assert "session=validsession" in response.headers["set-cookie"]
    assert f"expires={expire_tomorrow}" in response.headers["set-cookie"]


@mock.patch("jaanevis.requests.login_request.LoginRequest")
@mock.patch("jaanevis.usecases.login.LoginUseCase")
def test_login_invalid_credentials(mock_usecase, request_mock) -> None:
    body = {"username": "username", "password": "wrong_password"}
    mock_usecase().execute.return_value = (
        res.ResponseFailure.build_parameters_error(
            "auth error", code=res.StatusCode.invalid_username_or_password
        )
    )

    response = client.post(PREFIX + "/user/login", json=body)

    assert response.status_code == 401
    mock_usecase().execute.assert_called()
    assert response.json() == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.invalid_username_or_password,
        "message": "auth error",
    }


@mock.patch("jaanevis.usecases.authenticate.AuthenticateUseCase")
@mock.patch("jaanevis.requests.logout_request.LogoutRequest")
@mock.patch("jaanevis.usecases.logout.LogoutUseCase")
def test_logout_with_invalid_session(
    mock_usecase, mock_request, auth_usecase
) -> None:
    mock_usecase().execute.return_value = res.ResponseSuccess("validsession")
    session = uuid.uuid4()
    yesterday = datetime.now() - timedelta(days=1)
    expire_yesterday = yesterday.strftime("%a, %d %b %Y %H:%M:%S GMT")
    auth_usecase().execute.return_value = (
        res.ResponseFailure.build_parameters_error("invalid session")
    )
    req_obj = mock.Mock()
    mock_request.build.return_value = req_obj

    response = client.get(
        PREFIX + "/user/logout", headers={"cookie": f"session={session}"}
    )

    assert response.status_code == 200
    mock_usecase().execute.assert_called_with(req_obj)
    mock_request.build.assert_called_with(session=str(session))
    assert "set-cookie" in dict(response.headers)
    assert 'session="";' in response.headers["set-cookie"]
    assert f"expires={expire_yesterday}" in response.headers["set-cookie"]


@mock.patch("jaanevis.utils.mail.EmailHandler")
@mock.patch("jaanevis.requests.register_request.RegisterRequest")
@mock.patch("jaanevis.usecases.register.RegisterUseCase")
def test_register(mock_usecase, request_mock, mock_email) -> None:
    body = {"email": "a@a.com", "password": "password"}
    mock_usecase().execute.return_value = res.ResponseSuccess(
        {"type": "Success", "message": "activation email was sent"}
    )

    response = client.post(PREFIX + "/user/register", json=body)

    assert response.status_code == 200
    mock_usecase.assert_called_with(repo=mock.ANY, email_handler=mock_email())
    request_mock.build.assert_called_with(email="a@a.com", password="password")
    mock_usecase().execute.assert_called_with(request_mock.build())
    assert response.json() == {
        "type": "Success",
        "message": "activation email was sent",
    }


def test_register_with_invalid_email() -> None:
    pass


@mock.patch("jaanevis.requests.register_request.RegisterRequest")
@mock.patch("jaanevis.usecases.register.RegisterUseCase")
def test_register_with_invalid_password(mock_usecase, mock_request) -> None:
    body = {"email": "a@a.com", "password": "1234"}
    invalid_request = req.InvalidRequestObject(
        error_code=res.StatusCode.invalid_password
    )
    invalid_request.add_error(
        "password", "invalid password", code=res.StatusCode.invalid_password
    )
    mock_usecase().execute.return_value = (
        res.ResponseFailure.build_from_invalid_request_object(invalid_request)
    )

    response = client.post(PREFIX + "/user/register", json=body)

    assert response.status_code == 400
    mock_usecase().execute.assert_called()
    assert response.json() == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.invalid_password,
        "message": "password: invalid password",
    }


@mock.patch("jaanevis.requests.activate_user_request.ActivateUserRequest")
@mock.patch("jaanevis.usecases.activate_user.ActivateUserUseCase")
def test_user_activation(mock_usecase, mock_request) -> None:
    username = "a@a.com"
    activation_token = "token"

    response = client.get(
        PREFIX + f"/user/activate?username={username}&token={activation_token}"
    )

    assert response.status_code == 200
    mock_usecase.assert_called_with(repo=mock.ANY)
    mock_request.build.assert_called_with(
        username=username, token=activation_token
    )
    mock_usecase().execute.assert_called_with(mock_request.build())
