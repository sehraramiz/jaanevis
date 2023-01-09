from unittest import mock

from jaanevis.domain import user as u
from jaanevis.requests import auth_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import authenticate as uc


def test_authenticte_finds_correct_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(username="username")
    auth_header = "Basic dXNlcm5hbWU6cGFzc3dvcmQ="

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(token=auth_header)

    response = auth_usecase.execute(request_obj)

    repo.get_user_by_username.assert_called_with(username="username")
    assert response.value.username == "username"


def test_authenticte_response_unauthorized_on_invalid_auth_header() -> None:
    repo = mock.Mock()
    auth_header = "invalid header"

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(token=auth_header)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "header: Invalid auth header",
    }


def test_authenticte_response_unauthorized_on_empty_auth_header() -> None:
    repo = mock.Mock()
    auth_header = ""

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(token=auth_header)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "header: Invalid auth header",
    }


def test_authenticte_handles_non_existant_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None
    auth_header = "Basic dXNlcjox"

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(token=auth_header)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "message": "User not found",
    }
