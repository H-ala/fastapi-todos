from jose import jwt
from app.core.config import settings
import pytest


prefix = "/api/v1/auth"

async def test_login(client, test_user):
    user_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    res = await client.post(f"{prefix}/login", data=user_data)
    print("dlm", res.json())
    token_data = jwt.decode(
            res.json()["access_token"], 
            settings.SECRET_KEY,
            [settings.ALGORITHM]
        )
    print("slm", res.json())
    assert token_data["email"] == test_user["email"]
    assert res.status_code == 200


@pytest.mark.parametrize("username_or_email, password, status_code", [
    ("wrong_email@gmail.com", "123", 403),
    ("hos.ala81@gmail.com", "wrong_password", 403),
    ("wrong_email@gmail.com", "wrong_password", 403),
    ("wrong_username", "123", 403),
    ("hala", "wrong_password", 403),
    ("wrong_username", "wrong_password", 403),
    (None, "123", 403),
    ("hala", None, 403),
    ("hos.ala81@gmail.com", "123", 200),
    ("hala", "123", 200),
])
async def test_incorrect_login(client, test_user, username_or_email, password, status_code):
    user_data = { 
        "username": username_or_email,
        "password": password
    }
    res = await client.post(f"{prefix}/login", data=user_data)
    print(res.json())
    assert res.status_code == status_code

