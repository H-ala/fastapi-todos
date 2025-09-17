from jose import jwt
from app.core.config import settings
import pytest


prefix = "/api/v1/auth"

async def test_login(client, test_user):
    user_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    res = await client.post(f"{prefix}/login", json=user_data)
    token_data = jwt.decode(
            res.json()["access_token"], 
            settings.SECRET_KEY,
            [settings.ALGORITHM]
        )
    print("slm", res.json())
    assert token_data["email"] == test_user["email"]
    assert res.status_code == 200


@pytest.mark.parametrize("username, email, password, status_code", [
    (None, "wrong_email@gmail.com", "123", 404),
    (None, "hos.ala81@gmail.com", "wrong_password", 403),
    (None, "wrong_email@gmail.com", "wrong_password", 404),
    ("wrong_username", None, "123", 404),
    ("hala", None, "wrong_password", 403),
    ("wrong_username", None, "wrong_password", 404),
    (None, None, "123", 400),
    ("hala", "hos.ala81@gmail.com", "123", 200),
    ("wrong_username", "hos.ala81@gmail.com", "123", 200),
    ("hala", "wrong_email@gmail.com", "123", 200),
    ("hala", "hos.ala81@gmail.com", None, 422),
])
async def test_incorrect_login(client, test_user, username, email, password, status_code):
    user_data = { 
        "username": username,
        "email": email,
        "password": password
    }
    res = await client.post(f"{prefix}/login", json=user_data)
    # assert res.json() == {'message': 'Invalid email or password.', 'error_code': 'invalid_email_or_password', 'detail': ''}
    assert res.status_code == status_code

