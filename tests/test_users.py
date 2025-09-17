from app.schemas.user_schema import UserOut


prefix = "/api/v1/users/"

# def test_health_check(client):
#     res = client.get("/")
#     assert res.json().get("message") == "Hello World"
#     assert res.status_code == 200

async def test_create_user(client):
    payload = {
        "first_name": "Hosein",
        "last_name": "Ala",
        "username": "hala",
        "email": "hos.ala81@gmail.com", 
        "password": "123", 
        "repeat_password": "123" 
    }
    res = await client.post(prefix, json=payload)
    new_user = UserOut(**res.json()) 
    assert new_user.email == 'hos.ala81@gmail.com'
    assert res.status_code == 201



    