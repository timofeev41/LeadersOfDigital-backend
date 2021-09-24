import typing as tp

from fastapi import FastAPI

from modules.db.models.models import EmployeeEntry

api = FastAPI()

fake_data = [
    {"id": "23854332", "speciality": "Ведущий инженер", "salary": 38600},
    {"id": "23854336", "speciality": "Машинист", "salary": 25200},
    {"id": "23854539", "speciality": "заместитель главного инженера", "salary":151100},
    {"id": "23154332", "speciality": "based dep", "salary": 50000},
    {"id": "23854336", "speciality": "Заринус", "salary": 2500},
    {"id": "23854139", "speciality": "Андрюхус", "salary": 7500},
    {"id": "21852332", "speciality": "база", "salary": 12333},
    {"id": "23852336", "speciality": "Антонус", "salary": 500},
    {"id": "23853539", "speciality": "Егорус", "salary": 1200},
    {"id": "23844332", "speciality": "Приколист", "salary": 12005},
]


@api.get("/api/filter", response_model=tp.List[EmployeeEntry])
async def filter_employees(start: int, end: int) -> tp.Dict[str, tp.Any]:
    pass