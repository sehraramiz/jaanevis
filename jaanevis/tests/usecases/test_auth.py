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
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )
    repo.get_session_by_session_id.return_value = s.Session(
        email="a@a.com", session_id=session
    )

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=str(session))

    response = auth_usecase.execute(request_obj)

    repo.get_session_by_session_id.assert_called_with(session_id=str(session))
    repo.get_user_by_email.assert_called_with(email="a@a.com")
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
        "code": res.StatusCode.invalid_session,
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
        "code": res.StatusCode.invalid_session,
        "message": "session: Invalid session",
    }


def test_authenticte_handles_non_existant_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_email.return_value = None
    session = uuid.uuid4()

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "code": res.StatusCode.failure,
        "message": "User not found",
    }


def test_authenticte_handles_expired_session() -> None:
    repo = mock.Mock()
    repo.get_user_by_email.return_value = None
    session = uuid.uuid4()
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )
    expire_time = (datetime.now() - timedelta(hours=1)).timestamp()

    repo.get_session_by_session_id.return_value = s.Session(
        email="a@a.com", session_id=session, expire_time=expire_time
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
        "code": res.StatusCode.expired_session,
        "message": "Session expired",
    }


def test_logout_removes_existant_user_session() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )
    repo.get_session_by_session_id.return_value = s.Session(
        email="a@a.com", session_id=session
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
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )
    repo.get_session_by_session_id.return_value = None

    logout_usecase = logout_uc.LogoutUseCase(repo)
    request_obj = logout_req.LogoutRequest.build(session=str(session))

    response = logout_usecase.execute(request_obj)

    assert bool(response) is True


def test_logout_success_non_existent_user() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_email.return_value = None
    repo.get_session_by_session_id.return_value = s.Session(
        email="a@a.com", session_id=session
    )

    logout_usecase = logout_uc.LogoutUseCase(repo)
    request_obj = logout_req.LogoutRequest.build(session=str(session))

    response = logout_usecase.execute(request_obj)

    assert bool(response) is True


def test_authenticte_handles_deactive_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=False,
    )
    session = uuid.uuid4()
    repo.get_session_by_session_id.return_value = s.Session(
        email="a@a.com", session_id=session
    )

    auth_usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=session)

    response = auth_usecase.execute(request_obj)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.inactive_user,
        "message": "User is not active",
    }


def test_authenticate_handles_generic_error() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )
    repo.get_session_by_session_id.side_effect = Exception("An error message")

    usecase = uc.AuthenticateUseCase(repo)
    request_obj = req.AuthenticateRequest.build(session=str(session))

    response_obj = usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }


def test_logout_handles_generic_error() -> None:
    session = uuid.uuid4()
    repo = mock.Mock()
    repo.get_session_by_session_id.side_effect = Exception("An error message")

    usecase = logout_uc.LogoutUseCase(repo)
    request_obj = logout_req.LogoutRequest.build(session=str(session))

    response_obj = usecase.execute(request_obj)

    assert bool(response_obj) is False
    assert response_obj.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }
