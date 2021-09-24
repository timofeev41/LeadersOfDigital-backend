from pydantic import BaseModel
from enum import Enum


class EmployeeSex(str, Enum):
    male = "male"
    female = "female"


class EmployeeEntry(BaseModel):
    speciality: str
    birthDate: str
    gender: EmployeeSex
    is_married: bool
    startDate: str
    endDate: str
    absenceReason: str
    absenceDays: int
    salary: int
    city: str
    childrenCount: int


class DatabaseLinkModel(BaseModel):
    link: str
