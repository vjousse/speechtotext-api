import asyncio
from tortoise import Tortoise
from app.schemas.user import UserCreate
from app.schemas.asr_model import AsrModelCreate
from app.schemas.asr_model import Lang
from app.core.config import settings
from app.crud import asr_model_crud


async def create_asr_model(
        label: str, description: str, lang: Lang):

    asr_model_create = AsrModelCreate(
        label=label,
        description=description,
        lang=lang.value
    )

    await asr_model_crud.create(asr_model_create)


async def create_user(email="phil@phil.com", password="phil"):
    from app.services.fastapi_users import fastapi_users

    await fastapi_users.create_user(
        UserCreate(
            email=email,
            password=password,
        )
    )


async def main():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={'models': settings.TORTOISE_MODELS}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

    await create_user()
    await create_asr_model("fr.kaldi", "French Kaldi model", Lang.FR)
    await create_asr_model("en.kaldi", "English Kaldi model", Lang.EN)


asyncio.run(main())
