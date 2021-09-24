import typing as tp

from pydantic import BaseModel
from enum import Enum


class EmployeeSex(str, Enum):
    male = "male"
    female = "female"


class EmployeeEntry(BaseModel):
    id: str
    speciality: str
    birthDate: str
    gender: EmployeeSex
    is_married: bool
    startDate: str
    endDate: tp.Optional[str]
    absenceReason: tp.Optional[str]
    absenceDays: tp.Optional[int]
    salary: int
    city: str
    childrenCount: int
    is_fired: bool


class FilteringClass(BaseModel):
    speciality: tp.Optional[str]
    birthDate: tp.Optional[tp.Tuple[str, str]]
    gender: tp.Optional[EmployeeSex]
    is_married: tp.Optional[bool]
    startDate: tp.Optional[tp.Tuple[str, str]]
    endDate: tp.Optional[tp.Tuple[str, str]]
    absenceReason: tp.Optional[str]
    absenceDays: tp.Optional[str]
    salary: tp.Optional[tp.Tuple[int, int]]
    city: tp.Optional[str]
    childrenCount: tp.Optional[int]
    is_fired: tp.Optional[bool]
