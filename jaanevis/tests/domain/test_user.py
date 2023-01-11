from jaanevis.domain import user as u


def test_user_model_init() -> None:
    user = u.User(username="username", password="password")

    assert user.username == "username"
    assert user.password == "password"


def test_user_model_from_dict() -> None:
    user = u.User.from_dict(
        {
            "username": "username",
            "password": "password",
        }
    )

    assert user.username == "username"
    assert user.password == "password"


def test_user_model_to_dict() -> None:
    user = u.User(username="username", password="password")

    assert user.to_dict() == {
        "username": "username",
        "password": "password",
    }
