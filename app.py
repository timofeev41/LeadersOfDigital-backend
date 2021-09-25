import typing as tp

from fastapi import FastAPI

from modules.db.db import MongoDbWrapper
from modules.db.models.models import FilteringClass, EmployeeEntry
from modules.utils.ml import BaseClassifier

api = FastAPI()

fake_data = [
    {"id": "23854332", "speciality": "Ведущий инженер", "salary": 38600},
    {"id": "23854336", "speciality": "Машинист", "salary": 25200},
    {"id": "23854539", "speciality": "заместитель главного инженера", "salary": 151100},
    {"id": "23154332", "speciality": "based dep", "salary": 50000},
    {"id": "23854336", "speciality": "Заринус", "salary": 2500},
    {"id": "23854139", "speciality": "Андрюхус", "salary": 7500},
    {"id": "21852332", "speciality": "база", "salary": 12333},
    {"id": "23852336", "speciality": "Антонус", "salary": 500},
    {"id": "23853539", "speciality": "Егорус", "salary": 1200},
    {"id": "23844332", "speciality": "Приколист", "salary": 12005},
]


@api.get("/api/employees")
async def get_employees(count: int = 100):
    employees = await MongoDbWrapper().get_all_employees()
    return employees[:100]


@api.post("/api/employees/filter")
async def filter_employees(filter: FilteringClass):
    result = await MongoDbWrapper().get_matching_employees(dict(filter))
    predictions: tp.List[int] = BaseClassifier().predict([EmployeeEntry(**_) for _ in result])
    return [{"employee": result[i], "prediction": predictions[i]} for i in range(len(result))]


@api.post("/api/employees")
async def create_employee(employee: EmployeeEntry):
    data = dict(employee)
    fake_data.append(data)
    return data


@api.patch("/api/employee")
async def patch_employee_data(employee_id: str, new_data: EmployeeEntry):
    pass
