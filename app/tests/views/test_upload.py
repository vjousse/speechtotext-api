import os
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.models.user import UserModel
from app.models.asr_model import AsrModel
from app.views.file import current_active_user

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_file_upload(app: FastAPI,
                     client: TestClient,
                     db_verified_user: UserModel,
                     default_model: AsrModel) -> None:

    # Authenticate the user
    app.dependency_overrides[current_active_user] = \
        lambda: db_verified_user

    files = {'file': open(f"{dir_path}/../fixtures/fileupload.txt", 'r')}

    response = client.post(
        "/files/upload/",
        files=files,
        data={'asr_model_id': default_model.id}
    )

    print(response.text)

    assert response.json()["filename"] == "fileupload.txt"
    assert response.json()["user_id"] == str(db_verified_user.id)

    assert response.status_code == 201
