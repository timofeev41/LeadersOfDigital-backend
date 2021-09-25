import typing as tp

from pydantic import BaseModel
from enum import Enum


class EmployeeSex(str, Enum):
    male = "male"
    female = "female"


class EmployeeEducation(str, Enum):
    higher = "высшее"
    collage = "колледж"
    school = "шкила"


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
    education: EmployeeEducation


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
    start: int
    end: int


class FilteringClass(BaseModel):
    speciality: tp.Optional[str]
    birthDate: tp.Optional[BirthDateFilter]
    gender: tp.Optional[EmployeeSex]
    is_married: tp.Optional[bool]
    startDate: tp.Optional[StartDateFilter]
    endDate: tp.Optional[EndDateFilter]
    absenceReason: tp.Optional[str]
    absenceDays: tp.Optional[int]
    salary: tp.Optional[SalaryFilter]
    city: tp.Optional[str]
    childrenCount: tp.Optional[int]
    is_fired: tp.Optional[bool]
    education: tp.Optional[EmployeeEducation]
