import uuid
from datetime import datetime, timedelta
from unittest import mock

from freezegun import freeze_time

from jaanevis.domain import user as u
from jaanevis.requests import login_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import login as uc


@freeze_time(datetime.now())
def test_login_create_session_on_success() -> None:
    session_id = uuid.uuid4()
    repo = mock.Mock()

    with mock.patch("uuid.uuid4") as uuid_mock:
        uuid_mock.return_value = session_id
        repo.get_user_by_username.return_value = u.User(
            username="username", password="password"
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

    with mock.patch("uuid.uuid4") as uuid_mock:
        uuid_mock.return_value = session_id
        repo.get_user_by_username.return_value = u.User(
            username="username", password="password"
        )

        tomorrow = datetime.now() + timedelta(days=1)
        expire_tomorrow = tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT")

        login_usecase = uc.LoginUseCase(repo)
        login_request = req.LoginRequest(
            username="username", password="password"
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


def test_login_fails_on_wrong_password() -> None:
    repo = mock.Mock()
    user = u.User(username="username", password="password")

    repo.get_user_by_username.return_value = user

    login_usecase = uc.LoginUseCase(repo)
    login_request = req.LoginRequest(
        username="username", password="wrong password"
    )
    response = login_usecase.execute(login_request)

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
