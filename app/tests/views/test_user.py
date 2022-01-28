from fastapi.testclient import TestClient


def test_jwt_register_and_auth(client: TestClient) -> None:

    email = "phil@phil.com"
    password = "password"

    response = client.post(
        "/auth/register",
        json={"email": email, "password": password}
    )

    assert response.json()['email'] == "phil@phil.com"
    assert response.json()['is_active']
    assert not response.json()['is_superuser']
    assert response.status_code == 201

    response = client.post(
        "/auth/jwt/login",
        data={"username": email, "password": password}
    )

    assert response.status_code == 200
    assert response.json()['token_type'] == "bearer"
    assert "access_token" in response.json()
