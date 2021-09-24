import os
import typing as tp

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor

from modules.utils.singleton import SingletonMeta
from .models.models import EmployeeEntry, BaseModel


class MongoDbWrapper(metaclass=SingletonMeta):
    """A database wrapper implementation for MongoDB"""

    def __init__(self) -> None:
        """connect to database using credentials"""
        mongo_client_url: str = str(os.getenv("MONGO_CONNECTION_URL")) + "&ssl=true&ssl_cert_reqs=CERT_NONE"

        if mongo_client_url is None:
            message = "Cannot establish database connection: $MONGO_CONNECTION_URL environment variable is not set."
            raise IOError(message)

        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_client_url)

        self._database: AsyncIOMotorCursor = mongo_client["Hack"]

        # self._employees_data = self._database["Employees"]
        self._employees_data: AsyncIOMotorCollection = self._database["Testing"]

    @staticmethod
    async def _remove_ids(cursor: AsyncIOMotorCursor) -> tp.List[tp.Dict[str, tp.Any]]:
        """remove all MongoDB specific IDs from the resulting documents"""
        result: tp.List[tp.Dict[str, tp.Any]] = []
        for doc in await cursor.to_list(length=100):
            del doc["_id"]
            result.append(doc)
        return result

    @staticmethod
    async def _get_element_by_key(collection_: AsyncIOMotorCollection, key: str, value: str) -> tp.Dict[str, tp.Any]:
        result: tp.Dict[str, tp.Any] = await collection_.find_one({key: value}, {"_id": 0})
        return result

    async def _execute_all_from_collection(self, collection_: AsyncIOMotorCollection) -> tp.List[tp.Dict[str, tp.Any]]:
        cursor = collection_.find()
        return await self._remove_ids(cursor)

    async def push_to_collection(self, data: tp.List[tp.Dict[str, tp.Any]]) -> None:
        await self._employees_data.insert_many(data)
