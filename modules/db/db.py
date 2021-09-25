import logging
import os
import typing as tp

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor

from modules.utils.singleton import SingletonMeta
from .models.models import EmployeeEntry, BaseModel, BaseFilter
from modules.utils.utils import normalize_date


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

        # self._employees_data: AsyncIOMotorCollection = self._database["Employees_12"]
        self._employees_data: AsyncIOMotorCollection = self._database["Employees_latest"]

    @staticmethod
    async def _remove_ids(cursor: AsyncIOMotorCursor) -> tp.List[tp.Dict[str, tp.Any]]:
        """remove all MongoDB specific IDs from the resulting documents"""
        result: tp.List[tp.Dict[str, tp.Any]] = []
        for doc in await cursor.to_list(length=4000):
            del doc["_id"]
            data = doc.copy()
            data["birthDate"] = normalize_date(data["birthDate"])
            data["startDate"] = normalize_date(data["startDate"])
            result.append(data)
        return result

    @staticmethod
    async def _filter_elements_by_keys(
        collection_: AsyncIOMotorCollection, filter_: tp.Dict[str, tp.Any]
    ) -> AsyncIOMotorCursor:
        cursor: AsyncIOMotorCursor = collection_.find(filter_)
        return cursor

    async def _execute_all_from_collection(self, collection_: AsyncIOMotorCollection) -> tp.List[tp.Dict[str, tp.Any]]:
        cursor = collection_.find()
        return await self._remove_ids(cursor)

    @staticmethod
    async def _clear_filter(filter_: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        clean_filter = {}
        for key, value in filter_.items():
            if value is None:
                continue
            if isinstance(value, BaseFilter):
                clean_filter[key] = {"$gte": value.start, "$lte": value.end}
                continue
            clean_filter[key] = value
        return clean_filter

    async def push_employee_to_collection(self, data: tp.List[tp.Dict[str, tp.Any]]) -> None:
        await self._employees_data.insert_many(data)

    async def get_matching_employees(self, filter_: tp.Dict[str, tp.Any]) -> tp.List[tp.Dict[str, tp.Any]]:
        clean_filter = await self._clear_filter(filter_)
        cursor = await self._filter_elements_by_keys(self._employees_data, clean_filter)
        return await self._remove_ids(cursor)

    async def get_all_employees(self) -> tp.List[tp.Dict[str, tp.Any]]:
        return await self._execute_all_from_collection(self._employees_data)
