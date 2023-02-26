from datetime import datetime, timedelta
from unittest import mock

from freezegun import freeze_time

from jaanevis.domain import user as u
from jaanevis.requests import register_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import register as uc


def test_register_usecase_init() -> None:
    repo = mock.Mock()

    register_usecase = uc.RegisterUseCase(repo=repo)

    assert register_usecase.repo == repo


def test_register_handle_bad_request_invalid_email() -> None:
    repo = mock.Mock()

    request = req.RegisterRequest.build(
        email="", username="username", password=""
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.invalid_email,
        "message": "email: Invalid email",
    }


def test_register_handle_bad_request_invalid_username() -> None:
    repo = mock.Mock()

    request = req.RegisterRequest.build(
        email="a@a.com", username="", password="1234"
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.invalid_username,
        "message": "username: Invalid username, only use letters, numbers, underscores and periods.",
    }


def test_register_handle_existing_email() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None
    repo.get_user_by_email.return_value = u.User(
        email="a@a.com",
        username="username",
        password="22334455",
        is_active=True,
    )

    request = req.RegisterRequest.build(
        email="a@a.com", username="username", password="12345678"
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is False
    repo.get_user_by_email.assert_called_with(email="a@a.com")
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "code": res.StatusCode.user_exists,
        "message": "User with this email already exists",
    }


def test_register_handle_existing_username() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        email="a@a.com",
        username="username",
        password="22334455",
        is_active=True,
    )

    request = req.RegisterRequest.build(
        email="a@a.com", username="username", password="12345678"
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is False
    repo.get_user_by_username.assert_called_with(username="username")
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "code": res.StatusCode.user_exists,
        "message": "User with this username already exists",
    }


def test_register_handle_bad_request_invalid_password() -> None:
    repo = mock.Mock()

    request = req.RegisterRequest.build(
        email="a@a.com", username="username", password="1234"
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.invalid_password,
        "message": "password: minimum password length must be 8 characters",
    }


@mock.patch("jaanevis.utils.security.hash_password")
def test_register_creates_user(mock_hash) -> None:
    repo = mock.Mock()
    email, username, password = "a@a.com", "username", "22334455"
    user = u.User(email=email, username=username, password=password)
    hashed_password = "hashedpassword"
    user_res = u.UserRead(email=email, username=username, is_active=False)

    repo.get_user_by_username.return_value = None
    repo.get_user_by_email.return_value = None
    repo.create_user.return_value = user
    mock_hash.return_value = hashed_password

    request = req.RegisterRequest.build(
        email=email, username=username, password=password
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is True
    repo.create_user.assert_called_with(
        email=email, username=username, password=hashed_password
    )
    assert response.value == user_res


@freeze_time(datetime.now())
@mock.patch("secrets.token_urlsafe")
def test_register_creates_user_activation_session(mock_secrets) -> None:
    repo = mock.Mock()
    email, username, password = "a@a.com", "username", "22334455"
    user = u.User(email=email, username=username, password=password)
    secret_session = "secret_session"
    expire_time = (datetime.now() + timedelta(days=2)).timestamp()

    repo.get_user_by_username.return_value = None
    repo.get_user_by_email.return_value = None
    repo.create_user.return_value = user
    mock_secrets.return_value = secret_session

    request = req.RegisterRequest.build(
        email=email, username=username, password=password
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is True
    repo.create_session.assert_called_with(
        session_id=secret_session, username=email, expire_time=expire_time
    )


@mock.patch("jaanevis.utils.event.post_event")
@mock.patch("secrets.token_urlsafe")
def test_register_send_user_registered_event(mock_secrets, event_mock) -> None:
    repo = mock.Mock()
    email, username, password = "a@a.com", "username", "22334455"
    user = u.User(email=email, username=username, password=password)
    activation_token = "token"

    repo.get_user_by_username.return_value = None
    repo.get_user_by_email.return_value = None
    repo.create_user.return_value = user
    mock_secrets.return_value = activation_token

    request = req.RegisterRequest.build(
        email=email, username=username, password=password
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is True
    event_mock.assert_called_with(
        "user_registered",
        {"activation_token": activation_token, "email": email},
    )


@mock.patch("jaanevis.utils.security.hash_password")
def test_register_deletes_created_user_on_exception(mock_hash) -> None:
    repo = mock.Mock()
    email, username, password = "a@a.com", "username", "22334455"
    user = u.User(email=email, username=username, password=password)
    hashed_password = "hashedpassword"

    repo.get_user_by_username.return_value = None
    repo.get_user_by_email.return_value = None
    repo.create_user.return_value = user
    mock_hash.return_value = hashed_password
    repo.create_session.side_effect = Exception("some error")

    request = req.RegisterRequest.build(
        email=email, username=username, password=password
    )
    register_usecase = uc.RegisterUseCase(repo)
    response = register_usecase.execute(request)

    assert bool(response) is False
    repo.create_user.assert_called()
    repo.delete_user.assert_called_with(username=email)
