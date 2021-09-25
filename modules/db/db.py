import logging
import os
import random
import typing as tp
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor

from modules.utils.singleton import SingletonMeta
from .models.models import BaseFilter, StartDateFilter, BirthDateFilter, EndDateFilter, EmployeeEducation


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
            data["birthDate"] = data["birthDate"]
            data["startDate"] = data["startDate"]
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
        clean_filter: tp.Dict[tp.Any, tp.Any] = {}
        for key, value_ in filter_.items():
            if value_ is None:
                continue
            if isinstance(value_, BaseFilter):
                # Check if instance is Pydantic's filter Model
                if isinstance(value_, (BirthDateFilter, StartDateFilter, EndDateFilter)):
                    # Check if instance is Pydantic's between filter Model
                    print(value_)
                    clean_filter[key] = {
                        "$gte": datetime.fromisoformat(value_.start),
                        "$lte": datetime.fromisoformat(value_.end),
                    }
                    continue
                clean_filter[key] = {"$gte": value_.start, "$lte": value_.end}
                continue
            if isinstance(value_, list):
                # Check if instance is multiple choice field
                if isinstance(value_, EmployeeEducation):
                    # check if instance if a list of education level enums
                    clean_filter[key] = {"$in": [value_.value for _ in value_]}
                    continue
                clean_filter[key] = {"$in": value_}
                continue
            clean_filter[key] = value_
        print(clean_filter)
        return clean_filter

    async def push_employee_to_collection(self, data: tp.List[tp.Dict[str, tp.Any]]) -> None:
        await self._employees_data.insert_many(data)

    async def get_matching_employees(self, filter_: tp.Dict[str, tp.Any]) -> tp.List[tp.Dict[str, tp.Any]]:
        clean_filter = await self._clear_filter(filter_)
        cursor = await self._filter_elements_by_keys(self._employees_data, clean_filter)
        return await self._remove_ids(cursor)

    async def get_all_employees(self) -> tp.List[tp.Dict[str, tp.Any]]:
        return await self._execute_all_from_collection(self._employees_data)

    async def update_employee(self, key: str, value: str, new_value: str) -> None:
        await self._employees_data.update_one({key: value}, {"$set": {key: new_value}})

    async def _update_everywhere(self, key: str, value: str) -> None:
        data = await self._execute_all_from_collection(self._employees_data)
        for doc in data:
            await self._employees_data.update_one({"id": doc["id"]}, {"$set": {key: value}})
