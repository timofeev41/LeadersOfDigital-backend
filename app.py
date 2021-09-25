import typing as tp

from fastapi import FastAPI

from modules.db.db import MongoDbWrapper
from modules.db.models.models import FilteringClass, EmployeeEntry
from modules.ml.predictor_class import Analitics
from modules.ml.training import train
from starlette.middleware.cors import CORSMiddleware
import random

api = FastAPI()


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/api/employees")
async def get_employees(start: int = 0, count: int = 100) -> tp.List[tp.Dict[str, tp.Any]]:
    employees = await MongoDbWrapper().get_all_employees()
    return employees[start:count]


@api.post("/api/employees/filter")
async def filter_employees(filter: FilteringClass) -> tp.List[tp.Dict[str, tp.Any]]:
    result = await MongoDbWrapper().get_matching_employees(dict(filter))
    # predictions: tp.List[int] = Analitics([EmployeeEntry(**_) for _ in result]).predict()
    predictions = [random.randint(1, 5 * 1 << 10) for _ in range(0, len(result))]
    return [{"employee": result[i], "prediction": predictions[i]} for i in range(len(result))]


@api.post("/api/employees")
async def create_employee(employee: EmployeeEntry) -> tp.Dict[str, bool]:
    await MongoDbWrapper().push_employee_to_collection([dict(employee)])
    return {"status": True}


@api.get("/train")
async def train_model() -> tp.Dict[str, bool]:
    employees = await MongoDbWrapper().get_all_employees()
    train([EmployeeEntry(**_) for _ in employees])
    return {"status": True}
