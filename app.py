import typing as tp

from fastapi import FastAPI

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
async def filter_employees(start: tp.Optional[int], end: tp.Optional[int]):
    if not start or not end:
        return fake_data
    result: tp.List[tp.Dict[str, tp.Any]] = []
    for data in fake_data:
        if start <= data["salary"] <= end:
            result.append(data)
    return result


@api.post("/api/employees")
async def create_employee(id: str, speciality: str, salary: int):
    fake_data.append({"id": id, "speciality": speciality, "salary": salary})
    return {"id": id, "speciality": speciality, "salary": salary}
