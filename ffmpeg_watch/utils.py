import re
from typing import Sequence


def opt_val_of(opt: str,
               args: Sequence[str]) -> str:
    opt_idx = args.index(opt)
    opt_val = args[opt_idx+1]
    return opt_val


class HMS:
    pattern = re.compile(
        r"^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$"
    )

    def __init__(self,
                 hours: int,
                 minutes: int,
                 seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def total_seconds(self) -> int:
        return self.hours * 3600 + self.minutes * 60 + self.seconds

    def __gt__(self, other: 'HMS') -> bool:
        return self.total_seconds() > other.total_seconds()

    def __lt__(self, other: 'HMS') -> bool:
        return self.total_seconds() < other.total_seconds()

    def __int__(self) -> int:
        return self.total_seconds()

    def __sub__(self, other: 'HMS') -> 'HMS':
        total_seconds = self.total_seconds() - other.total_seconds()

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = (total_seconds % 3600) % 60

        return HMS(hours, minutes, seconds)

    def __str__(self) -> str:
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"


def hms(value: str) -> HMS:
    if not HMS.pattern.match(value):
        raise ValueError('Invalid time format. Please provide time in HH:MM:SS format.')

    hh, mm, ss = map(int, value.split(':'))
    return HMS(hh, mm, ss)
