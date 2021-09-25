import datetime
import typing as tp

from pydantic import BaseModel
from enum import Enum


class EmployeeSex(str, Enum):
    male = "male"
    female = "female"


class EmployeeEducation(str, Enum):
    higher = "higher"
    college = "college"
    school = "school"


class EmployeeEntry(BaseModel):
    id: str
    speciality: str
    birthDate: datetime.datetime
    gender: EmployeeSex
    is_married: bool
    startDate: datetime.datetime
    endDate: tp.Optional[datetime.datetime]
    absenceReason: tp.Optional[str]
    absenceDays: tp.Optional[int]
    salary: int
    city: str
    childrenCount: int
    is_fired: bool
    education: EmployeeEducation
    mentored: bool


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


class ChildrenFilter(BaseFilter):
    start: int
    end: int


class AbsenceFilter(BaseFilter):
    start: int
    end: int


class FilteringClass(BaseModel):
    speciality: tp.Optional[tp.List[str]]
    birthDate: tp.Optional[BirthDateFilter]
    gender: tp.Optional[EmployeeSex]
    is_married: tp.Optional[bool]
    startDate: tp.Optional[StartDateFilter]
    endDate: tp.Optional[EndDateFilter]
    absenceReason: tp.Optional[str]
    absenceDays: tp.Optional[AbsenceFilter]
    salary: tp.Optional[SalaryFilter]
    city: tp.Optional[tp.List[str]]
    childrenCount: tp.Optional[ChildrenFilter]
    is_fired: tp.Optional[bool]
    education: tp.Optional[tp.List[EmployeeEducation]]
    mentored: tp.Optional[bool]
