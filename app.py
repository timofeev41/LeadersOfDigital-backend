import typing as tp

from fastapi import FastAPI

from modules.db.db import MongoDbWrapper
from modules.db.models.models import FilteringClass, EmployeeEntry
from modules.ml.predictor_class import Analitics
from modules.ml.training import train
from starlette.middleware.cors import CORSMiddleware

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/api/employees")
async def get_employees(start: int = 0, count: int = 100):
    employees = await MongoDbWrapper().get_all_employees()
    return employees[start:count]


@api.post("/api/employees/filter")
async def filter_employees(filter: FilteringClass):
    result = await MongoDbWrapper().get_matching_employees(dict(filter))
    predictions: tp.List[int] = Analitics([EmployeeEntry(**_) for _ in result]).predict()
    return [{"employee": result[i], "prediction": predictions[i]} for i in range(len(result))]


@api.post("/api/employees")
async def create_employee(employee: EmployeeEntry):
    await MongoDbWrapper().push_employee_to_collection([dict(employee)])
    return {"status": True}


@api.patch("/api/upload")
async def add_education():
    pass


@api.patch("/api/employee")
async def patch_employee_data(employee_id: str, new_data: EmployeeEntry):
    pass


@api.get("/train")
async def trainer():
    employees = await MongoDbWrapper().get_all_employees()
    train([EmployeeEntry(**_) for _ in employees])
