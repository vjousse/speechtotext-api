import os
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.models.user import UserModel
from app.models.asr_model import AsrModel
from app.views.file import current_active_user

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_file_upload(
    app: FastAPI,
    client: TestClient,
    db_verified_user: UserModel,
    default_model: AsrModel,
) -> None:

    # Authenticate the user
    app.dependency_overrides[current_active_user] = lambda: db_verified_user

    # See https://docs.python-requests.org/en/latest/user/advanced/
    # #post-multiple-multipart-encoded-files for more documentation
    multiple_files = [
        ("files", open(f"{dir_path}/../fixtures/fileupload.txt", "rb")),
        ("files", open(f"{dir_path}/../fixtures/fileupload.txt", "rb")),
    ]

    response = client.post(
        "/files/upload/",
        data={"asr_model_id": default_model.id},
        files=multiple_files,
    )

    json = response.json()

    assert len(json) == 2
    assert json[0]["filename"] == "fileupload.txt"
    assert json[1]["filename"] == "fileupload.txt"
    assert json[0]["user_id"] == str(db_verified_user.id)
    assert json[1]["user_id"] == str(db_verified_user.id)

    assert response.status_code == 201
