import random

from modules.db.models.models import EmployeeEntry
from modules.utils.singleton import SingletonMeta


class BaseClassifier(SingletonMeta):
    def predict(self, employee: list[EmployeeEntry]):
        return [random.randint(1, 365) for _ in range(0, len(employee))]
