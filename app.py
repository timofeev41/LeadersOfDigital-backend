from fastapi import FastAPI
from modules.db.db import MongoDbWrapper
from modules.utils.models import DatabaseLinkModel

api = FastAPI()


@api.get("/api/v1/upload_docs")
async def upload_docs(model: DatabaseLinkModel):
    dataset_link: str = model.link

    await MongoDbWrapper().push_to_collection()
