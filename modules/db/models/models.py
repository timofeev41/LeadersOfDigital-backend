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


class BaseFilter(BaseModel):
    start: str
    end: str


class BirthDateFilter(BaseFilter):
    pass


class StartDateFilter(BaseFilter):
    pass


class EndDateFilter(BaseFilter):
    pass


class SalaryFilter(BaseFilter):
    pass


class FilteringClass(BaseModel):
    speciality: tp.Optional[str]
    birthDate: tp.Optional[BirthDateFilter]
    gender: tp.Optional[EmployeeSex]
    is_married: tp.Optional[bool]
    startDate: tp.Optional[StartDateFilter]
    endDate: tp.Optional[EndDateFilter]
    absenceReason: tp.Optional[str]
    absenceDays: tp.Optional[str]
    salary: tp.Optional[SalaryFilter]
    city: tp.Optional[str]
    childrenCount: tp.Optional[int]
    is_fired: tp.Optional[bool]
