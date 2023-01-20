import uuid
from datetime import datetime, timedelta
from unittest import mock

from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.requests import auth_request as req
from jaanevis.requests import logout_request as logout_req
from jaanevis.responses import response as res
from jaanevis.usecases import authenticate as uc
from jaanevis.usecases import logout as logout_uc


def test_authenticte_finds_correct_user() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        username="username", password="password", is_active=True
    )
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


def test_authenticte_handles_expired_session() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None
    session = uuid.uuid4()
    repo.get_user_by_username.return_value = u.User(
        username="username", password="password", is_active=True
    )
    expire_time = (datetime.now() - timedelta(hours=1)).timestamp()

    repo.get_session_by_session_id.return_value = s.Session(
        username="username", session_id=session, expire_time=expire_time
    )

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    repo.delete_session_by_session_id.assert_called_with(
        session_id=str(session)
    )
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "Session expired",
    }


def test_logout_removes_existant_user_session() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        username="username", password="password", is_active=True
    )
    repo.get_session_by_session_id.return_value = s.Session(
        username="username", session_id=session
    )

    logout_usecase = logout_uc.LogoutUseCase(repo)
    request_obj = logout_req.LogoutRequest.build(session=str(session))

    response = logout_usecase.execute(request_obj)

    assert bool(response) is True
    repo.delete_session_by_session_id.assert_called_with(
        session_id=str(session)
    )


def test_logout_success_non_existent_session() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        username="username", password="password", is_active=True
    )
    repo.get_session_by_session_id.return_value = None

    logout_usecase = logout_uc.LogoutUseCase(repo)
    request_obj = logout_req.LogoutRequest.build(session=str(session))

    response = logout_usecase.execute(request_obj)

    assert bool(response) is True


def test_logout_success_non_existent_user() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None
    repo.get_session_by_session_id.return_value = s.Session(
        username="username", session_id=session
    )

    logout_usecase = logout_uc.LogoutUseCase(repo)
    request_obj = logout_req.LogoutRequest.build(session=str(session))

    response = logout_usecase.execute(request_obj)

    assert bool(response) is True


def test_authenticte_handles_deactive_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        username="username", password="password", is_active=False
    )
    session = uuid.uuid4()
    repo.get_session_by_session_id.return_value = s.Session(
        username="username", session_id=session
    )

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "User is not active",
    }
