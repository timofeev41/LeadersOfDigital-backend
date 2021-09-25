import random

from modules.db.models.models import EmployeeEntry
from modules.utils.singleton import SingletonMeta


class BaseClassifier(metaclass=SingletonMeta):
    def predict(self, employee: list[EmployeeEntry]):
        return [random.randint(1, 5 * 1 << 10) for _ in range(0, len(employee))]
