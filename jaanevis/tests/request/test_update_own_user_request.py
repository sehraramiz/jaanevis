from jaanevis.domain import user as u
from jaanevis.requests import update_own_user_request as req

user = u.User(username="username", password="password")


def test_build_user_update_request() -> None:
    user = u.User(username="default", password="password", is_active=True)
    update_user = u.UserUpdateApi(username="username")
    request = req.UpdateOwnUserRequest.build(
        update_user=update_user, user=user
    )

    assert request.user == user
    assert request.update_user == update_user
    assert bool(request) is True


def test_build_own_user_update_from_wrong_type_user() -> None:
    request = req.UpdateOwnUserRequest.build(update_user=None, user=user)

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "body"


def test_build_user_update_from_invalid_user() -> None:
    update_user = u.UserUpdateApi(username="username")
    request = req.UpdateOwnUserRequest.build(
        update_user=update_user, user=None
    )

    assert bool(request) is False
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "user"
