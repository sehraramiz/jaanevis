from jaanevis.domain import user as u


def test_user_model_init() -> None:
    user = u.User(username="username", password="password", is_active=True)

    assert user.username == "username"
    assert user.password == "password"
    assert user.is_active is True


def test_user_model_from_dict() -> None:
    user = u.User.from_dict(
        {
            "username": "username",
            "password": "password",
            "is_active": True,
        }
    )

    assert user.username == "username"
    assert user.password == "password"
    assert user.is_active is True


def test_user_model_to_dict() -> None:
    user = u.User(username="username", password="password", is_active=True)

    assert user.to_dict() == {
        "username": "username",
        "password": "password",
        "is_active": True,
    }
