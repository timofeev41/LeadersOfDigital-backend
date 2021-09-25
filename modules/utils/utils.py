from datetime import datetime


def normalize_date(date: str, fmt: str = "%m/%d/%Y") -> datetime:
    return datetime.strptime(date, fmt)
