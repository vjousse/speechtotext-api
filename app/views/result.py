from fastapi import APIRouter, File, Form, UploadFile
from app.schemas.result import Result, ResultCreate
from app.crud import result_crud

result_views = APIRouter()


@result_views.post("/", response_model=Result)
async def create(
    filename: str = Form(...),
    message_id: str = Form(...),
    file: UploadFile = File(...),
):

    result_create = ResultCreate(message_id=message_id, filename=filename)

    result = await result_crud.create(result_create)

    await result_crud.move_to_upload(result_create, file)

    return result
