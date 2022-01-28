from fastapi.testclient import TestClient
from app.core.config import settings


def test_home(client: TestClient) -> None:

    response = client.get("/infos")
    assert response.status_code == 200
    assert response.json() == {
        "allowed_mimetypes": settings.ALLOWED_MIMETYPES
    }
