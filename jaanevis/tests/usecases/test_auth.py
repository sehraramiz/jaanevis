import uuid
from unittest import mock

from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.requests import auth_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import authenticate as uc


def test_authenticte_finds_correct_user() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(username="username")
    repo.get_session_by_session_id.return_value = s.Session(
        username="username", session_id=session
    )

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=str(session))

    response = auth_usecase.execute(request_obj)

    repo.get_session_by_session_id.assert_called_with(session_id=str(session))
    repo.get_user_by_username.assert_called_with(username="username")
    assert response.value.username == "username"


def test_authenticte_response_unauthorized_on_invalid_session() -> None:
    repo = mock.Mock()
    session = "invalidsession"
    repo.get_session_by_session_id.return_value = None

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "message": "Session not found",
    }


def test_authenticte_response_unauthorized_on_empty_session() -> None:
    repo = mock.Mock()
    session = ""

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "session: Invalid session",
    }


def test_authenticte_handles_non_existant_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None
    session = uuid.uuid4()

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "message": "User not found",
    }
