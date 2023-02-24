from unittest import mock

import pytest

from jaanevis.domain import user as u
from jaanevis.requests import update_own_user_request as req
from jaanevis.responses import response as res
from jaanevis.usecases import update_own_user as uc


@pytest.fixture
def user() -> u.User:
    return u.User(username="username", password="password", is_active=True)


def test_update_own_user() -> None:
    repo = mock.Mock()
    repo.get_user_by_username.return_value = None
    user = u.User(username="username", password="password")
    new_username = "new_username"
    user_read = u.UserRead(username=new_username, is_active=True)

    user_update = u.UserUpdateApi(username=new_username)
    updated_user = user
    updated_user.is_active = True
    updated_user.username = new_username
    repo.update_user.return_value = updated_user

    update_user_usecase = uc.UpdateOwnUserUseCase(repo)
    update_user_request = req.UpdateOwnUserRequest.build(
        update_user=user_update, user=user
    )

    response = update_user_usecase.execute(update_user_request)

    assert bool(response) is True
    repo.update_user.assert_called_with(obj=user, data={"username": new_username})
    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.value == user_read


def test_own_user_update_handles_invalid_user(user: u.User) -> None:
    repo = mock.Mock()
    user = u.User(username="username", password="password")

    update_user_usecase = uc.UpdateOwnUserUseCase(repo)
    update_user_request = req.UpdateOwnUserRequest.build(
        update_user=None, user=user
    )

    response = update_user_usecase.execute(update_user_request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.PARAMETERS_ERROR,
        "code": res.StatusCode.failure,
        "message": "body: Invalid user type",
    }


def test_update_user_handles_generic_error(user: u.User) -> None:
    repo = mock.Mock()
    repo.get_user_by_username.side_effect = Exception("An error message")
    user = u.User(username="username", password="password")

    new_username = "new_username"
    user_update = u.UserUpdateApi(username=new_username)

    update_user_usecase = uc.UpdateOwnUserUseCase(repo)
    update_user_request = req.UpdateOwnUserRequest.build(
        update_user=user_update, user=user
    )

    response = update_user_usecase.execute(update_user_request)

    assert bool(response) is False
    assert response.value == {
        "type": res.ResponseFailure.SYSTEM_ERROR,
        "code": res.StatusCode.failure,
        "message": "Exception: An error message",
    }
