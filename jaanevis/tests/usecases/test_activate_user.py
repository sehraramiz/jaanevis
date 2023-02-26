from unittest import mock

from jaanevis.domain import user as u
from jaanevis.requests import activate_user_request as req
from jaanevis.responses import ResponseFailure, StatusCode
from jaanevis.usecases import activate_user as uc


def test_activate_user_handle_invalid_request() -> None:
    repo = mock.Mock()

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username=None, token="token")
    response = usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseFailure.PARAMETERS_ERROR,
        "code": StatusCode.failure,
        "message": "username: Username can not be empty",
    }


def test_activate_user_handle_non_existent_token() -> None:
    repo = mock.Mock()
    repo.get_session_by_session_id_and_username.return_value = None

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username="username", token="token")
    response = usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseFailure.PARAMETERS_ERROR,
        "code": StatusCode.invalid_activation_token,
        "message": "Invalid activation token",
    }


def test_activate_user_handle_non_existent_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username="username", token="token")
    response = usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseFailure.RESOURCE_ERROR,
        "code": StatusCode.failure,
        "message": "User not found",
    }


def test_activate_user_handle_active_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username="username", token="token")
    response = usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseFailure.PARAMETERS_ERROR,
        "code": StatusCode.failure,
        "message": "User is already activated",
    }


def test_activate_user() -> None:
    repo = mock.Mock()
    user = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=False,
    )
    updated_user = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )
    user_result = u.UserRead(username="username", is_active=True)

    repo.get_user_by_username.return_value = user
    repo.update_user.return_value = updated_user

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username="username", token="token")
    response = usecase.execute(request)

    assert bool(response) is True
    repo.update_user.assert_called()
    assert response.value == user_result


def test_delete_session_after_user_activation() -> None:
    repo = mock.Mock()
    user = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=False,
    )
    updated_user = u.User(
        email="a@a.com",
        username="username",
        password="password",
        is_active=True,
    )

    repo.get_user_by_username.return_value = user
    repo.update_user.return_value = updated_user

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username="username", token="token")
    response = usecase.execute(request)

    assert bool(response) is True
    repo.delete_session_by_session_id.assert_called_with(session_id="token")


def test_activate_user_handles_generic_error() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.side_effect = Exception("An error message")

    usecase = uc.ActivateUserUseCase(repo)
    request = req.ActivateUserRequest.build(username="username", token="token")
    response = usecase.execute(request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseFailure.SYSTEM_ERROR,
        "code": StatusCode.failure,
        "message": "Exception: An error message",
    }
