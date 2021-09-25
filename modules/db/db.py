import logging
import os
import random
import typing as tp
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor

from modules.utils.singleton import SingletonMeta
from .models.models import BaseFilter, StartDateFilter, BirthDateFilter, EndDateFilter, \
    EmployeeEducation, ChildrenFilter


class MongoDbWrapper(metaclass=SingletonMeta):
    """Обертка для базы данных MongoDB, использующая паттерн Синглтон"""

    def __init__(self) -> None:
        """
        Инициализация базы данных и подключение к MongoDB

        Важно: Переменная окружения MONGO_CONNECTION_URL должна ссылку на подключение к MongoDB
        """
        mongo_client_url: str = str(os.getenv("MONGO_CONNECTION_URL")) + "&ssl=true&ssl_cert_reqs=CERT_NONE"

        if mongo_client_url is None:
            message = "Cannot establish database connection: $MONGO_CONNECTION_URL environment variable is not set."
            raise IOError(message)

        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_client_url)

        self._database: AsyncIOMotorCursor = mongo_client["Hack"]
        self._employees_data: AsyncIOMotorCollection = self._database["Employees_latest"]

    @staticmethod
    async def _remove_ids(cursor: AsyncIOMotorCursor) -> tp.List[tp.Dict[str, tp.Any]]:
        """Удалить все специфические для MongoDB значения (напр. _id)"""
        result: tp.List[tp.Dict[str, tp.Any]] = []
        for doc in await cursor.to_list(length=4000):
            del doc["_id"]
            data = doc.copy()
            result.append(data)
        return result

    @staticmethod
    async def _filter_elements_by_keys(
        collection_: AsyncIOMotorCollection, filter_: tp.Dict[str, tp.Any]
    ) -> AsyncIOMotorCursor:
        """Получить все найденные элементы из коллекции по ключу и значению"""
        cursor: AsyncIOMotorCursor = collection_.find(filter_)
        return cursor

    async def _execute_all_from_collection(self, collection_: AsyncIOMotorCollection) -> tp.List[tp.Dict[str, tp.Any]]:
        """Получить все элементы из коллекции"""
        cursor = collection_.find()
        return await self._remove_ids(cursor)

    @staticmethod
    async def _clear_filter(filter_: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        """Перевести модель Pydantic в словарь, сделать из этого запрос"""
        clean_filter: tp.Dict[tp.Any, tp.Any] = {}
        for key, value_ in filter_.items():
            if value_ is None:
                continue
            if isinstance(value_, BaseFilter):
                # Проверить, что переменная является Pydantic-моделью фильтром
                if isinstance(value_, (BirthDateFilter, StartDateFilter, EndDateFilter)):
                    # Проверить, что переменная является Pydantic-моделью со счетчиком
                    print(value_)
                    clean_filter[key] = {
                        "$gte": datetime.fromisoformat(value_.start),
                        "$lte": datetime.fromisoformat(value_.end),
                    }
                    continue
                clean_filter[key] = {"$gte": value_.start, "$lte": value_.end}
                continue
            if isinstance(value_, list):
                # Проверить, что переменная является полем множественного выбора
                if isinstance(value_, EmployeeEducation):
                    # Проверить, что переменная является Pydantic-моделью фильтром
                    clean_filter[key] = {"$in": [value_.value for _ in value_]}
                    continue
                clean_filter[key] = {"$in": value_}
                continue
            clean_filter[key] = value_
        return clean_filter

    async def push_employee_to_collection(self, data: tp.List[tp.Dict[str, tp.Any]]) -> None:
        """Добавить все элементы из листа в MongoDB"""
        await self._employees_data.insert_many(data)

    async def get_matching_employees(self, filter_: tp.Dict[str, tp.Any]) -> tp.List[tp.Dict[str, tp.Any]]:
        """Получить сотрудника(-ов) по фильтру"""
        clean_filter = await self._clear_filter(filter_)
        cursor = await self._filter_elements_by_keys(self._employees_data, clean_filter)
        return await self._remove_ids(cursor)

    async def get_all_employees(self) -> tp.List[tp.Dict[str, tp.Any]]:
        """Получить список всех сотрудников"""
        return await self._execute_all_from_collection(self._employees_data)

    async def update_employee(self, key: str, value: str, new_value: str) -> None:
        """Обновить данные о сотруднике"""
        await self._employees_data.update_one({key: value}, {"$set": {key: new_value}})

    async def _update_everywhere(self, key: str, value: str) -> None:
        """Обновить данные в КАЖДОМ элементе"""
        data = await self._execute_all_from_collection(self._employees_data)
        for doc in data:
            await self._employees_data.update_one({"id": doc["id"]}, {"$set": {key: value}})
