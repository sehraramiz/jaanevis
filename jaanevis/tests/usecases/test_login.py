import uuid
from datetime import datetime, timedelta
from unittest import mock

from freezegun import freeze_time

from jaanevis.domain import user as u
from jaanevis.requests import login_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import login as uc
from jaanevis.utils.security import hash_password


@freeze_time(datetime.now())
def test_login_create_session_on_success() -> None:
    session_id = uuid.uuid4()
    repo = mock.Mock()
    password = "password"
    hashed_password = hash_password(password)

    with mock.patch("uuid.uuid4") as uuid_mock:
        uuid_mock.return_value = session_id
        repo.get_user_by_username.return_value = u.User(
            email="a@a.com",
            username="username",
            password=hashed_password,
            is_active=True,
        )
        tomorrow = datetime.now() + timedelta(days=1)

        login_usecase = uc.LoginUseCase(repo)
        login_request = req.LoginRequest(
            username="username", password="password"
        )
        response = login_usecase.execute(login_request)

        assert bool(response) is True
        repo.get_user_by_username.assert_called_with(username="username")
        repo.create_or_update_session.assert_called_with(
            username="username",
            session_id=str(session_id),
            expire_time=tomorrow.timestamp(),
        )
        assert len(response.value) > 0


@freeze_time(datetime.now())
def test_login_create_session_with_correct_expire_time() -> None:
    session_id = uuid.uuid4()
    repo = mock.Mock()
    password = "password"
    hashed_password = hash_password(password)

    with mock.patch("uuid.uuid4") as uuid_mock:
        uuid_mock.return_value = session_id
        repo.get_user_by_username.return_value = u.User(
            email="a@a.com",
            username="username",
            password=hashed_password,
            is_active=True,
        )

        tomorrow = datetime.now() + timedelta(days=1)
        expire_tomorrow = tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT")

        login_usecase = uc.LoginUseCase(repo)
        login_request = req.LoginRequest(
            username="username", password=password
        )
        response = login_usecase.execute(login_request)

        assert bool(response) is True
        repo.create_or_update_session.assert_called_with(
            username="username",
            session_id=str(session_id),
            expire_time=tomorrow.timestamp(),
        )
        assert response.value["expires"] == str(expire_tomorrow)


def test_login_fails_on_non_existant_user() -> None:
    repo = mock.Mock()

    repo.get_user_by_username.return_value = None

    login_usecase = uc.LoginUseCase(repo)
    login_request = req.LoginRequest(username="username", password="password")
    response = login_usecase.execute(login_request)

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.code == res.StatusCode.invalid_username_or_password


def test_login_fails_on_wrong_password() -> None:
    repo = mock.Mock()
    user = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )

    repo.get_user_by_username.return_value = user

    login_usecase = uc.LoginUseCase(repo)
    login_request = req.LoginRequest(
        username="username", password="wrong password"
    )
    response = login_usecase.execute(login_request)

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.code == res.StatusCode.invalid_username_or_password


@mock.patch("jaanevis.utils.security.verify_password")
def test_login_fails_on_inactive_user(pass_verify_mock) -> None:
    repo = mock.Mock()
    user = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=False,
    )

    repo.get_user_by_username.return_value = user

    login_usecase = uc.LoginUseCase(repo)
    login_request = req.LoginRequest(username="username", password="password")
    response = login_usecase.execute(login_request)

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.inactive_user,
        "message": "User is not active",
    }


def test_login_handles_generic_error() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.side_effect = Exception("An error message")

    login_usecase = uc.LoginUseCase(repo)
    login_request = req.LoginRequest(username="username", password="password")
    response = login_usecase.execute(login_request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }
