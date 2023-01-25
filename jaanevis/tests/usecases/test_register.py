from datetime import datetime, timedelta
from unittest import mock

from freezegun import freeze_time

from jaanevis.config import settings
from jaanevis.domain import user as u
from jaanevis.requests import register_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import register as uc


def test_register_usecase_init() -> None:
    repo = mock.Mock()
    email_handler = mock.Mock()

    register_usecase = uc.RegisterUseCase(
        repo=repo, email_handler=email_handler
    )

    assert register_usecase.repo == repo
    assert register_usecase.email_handler == email_handler


def test_register_handle_bad_request_invalid_email() -> None:
    repo = mock.Mock()
    email_handler = mock.Mock()

    request = req.RegisterRequest.build(email="", password="")
    register_usecase = uc.RegisterUseCase(repo, email_handler=email_handler)
    response = register_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "email: Invalid email",
    }


def test_register_handle_existing_email() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        username="a@a.com", password="22334455", is_active=True
    )
    email_handler = mock.Mock()

    request = req.RegisterRequest.build(email="a@a.com", password="12345678")
    register_usecase = uc.RegisterUseCase(repo, email_handler=email_handler)
    response = register_usecase.execute(request)

    assert bool(response) is False
    repo.get_user_by_username.assert_called_with(username="a@a.com")
    assert response.value == {
        "type": res.ResponseFailure.RESOURCE_ERROR,
        "message": "User with this email already exists",
    }


def test_register_handle_bad_request_invalid_password() -> None:
    repo = mock.Mock()
    email_handler = mock.Mock()

    request = req.RegisterRequest.build(email="a@a.com", password="1234")
    register_usecase = uc.RegisterUseCase(repo, email_handler=email_handler)
    response = register_usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "message": "password: minimum password length must be 8 characters",
    }


@mock.patch("jaanevis.utils.security.hash_password")
def test_register_creates_user(mock_hash) -> None:
    repo = mock.Mock()
    email_handler = mock.Mock()
    email, password = "a@a.com", "22334455"
    user = u.User(username=email, password=password)
    hashed_password = "hashedpassword"
    user_res = u.UserRead(username=email, is_active=False)

    repo.get_user_by_username.return_value = None
    repo.create_user.return_value = user
    mock_hash.return_value = hashed_password

    request = req.RegisterRequest.build(email=email, password=password)
    register_usecase = uc.RegisterUseCase(repo, email_handler=email_handler)
    response = register_usecase.execute(request)

    assert bool(response) is True
    repo.create_user.assert_called_with(
        username=email, password=hashed_password
    )
    assert response.value == user_res


@freeze_time(datetime.now())
@mock.patch("secrets.token_urlsafe")
def test_register_creates_user_activation_session(mock_secrets) -> None:
    repo = mock.Mock()
    email_handler = mock.Mock()
    email, password = "a@a.com", "22334455"
    user = u.User(username=email, password=password)
    secret_session = "secret_session"
    expire_time = (datetime.now() + timedelta(days=2)).timestamp()

    repo.get_user_by_username.return_value = None
    repo.create_user.return_value = user
    mock_secrets.return_value = secret_session

    request = req.RegisterRequest.build(email=email, password=password)
    register_usecase = uc.RegisterUseCase(repo, email_handler=email_handler)
    response = register_usecase.execute(request)

    assert bool(response) is True
    repo.create_session.assert_called_with(
        session_id=secret_session, username=email, expire_time=expire_time
    )


@mock.patch("secrets.token_urlsafe")
def test_register_send_activation_email(mock_secrets) -> None:
    repo = mock.Mock()
    email_handler = mock.Mock()
    email, password = "a@a.com", "22334455"
    user = u.User(username=email, password=password)
    activation_token = "token"
    activation_url = f"{settings.PROJECT_URL}{settings.API_V1_STR}/user/activate?username={email}&token={activation_token}"
    mail_text = f"visit this link to activate your account {activation_url}"
    mail_subject = "Jaanevis Account Activation"

    repo.get_user_by_username.return_value = None
    repo.create_user.return_value = user
    mock_secrets.return_value = activation_token

    request = req.RegisterRequest.build(email=email, password=password)
    register_usecase = uc.RegisterUseCase(repo, email_handler=email_handler)
    response = register_usecase.execute(request)

    assert bool(response) is True
    email_handler.send_email.assert_called_with(
        email_to=email, text=mail_text, subject=mail_subject
    )
