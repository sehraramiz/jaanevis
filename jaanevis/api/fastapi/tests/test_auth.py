from unittest import mock

from fastapi.testclient import TestClient

from jaanevis.api.fastapi.main import app
from jaanevis.responses import response as res

client = TestClient(app)


@mock.patch("jaanevis.requests.login_request.LoginRequest")
@mock.patch("jaanevis.usecases.login.LoginUseCase")
def test_login(mock_usecase, request_mock) -> None:
    body = {"username": "username", "password": "password"}
    mock_usecase().execute.return_value = res.ResponseSuccess("validsession")

    response = client.post("/login", json=body)

    assert response.status_code == 200
    mock_usecase().execute.assert_called()
    request_mock.build.assert_called_with(
        username="username", password="password"
    )
    assert "set-cookie" in dict(response.headers)
    assert "session=validsession" in response.headers["set-cookie"]
