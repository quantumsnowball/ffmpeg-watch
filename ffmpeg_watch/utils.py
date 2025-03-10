import json
import re
import subprocess
from pathlib import Path
from typing import Any, Sequence


def opt_val_of(opt: str,
               args: Sequence[str]) -> str:
    try:
        opt_idx = args.index(opt)
        opt_val = args[opt_idx+1]
    except Exception:
        raise ValueError(f'Failed to parse value for {opt}')
    else:
        return opt_val


def get_video_duration(file: Path) -> float:
    # ffprobe
    cmd = ('ffprobe',
           '-v', 'quiet',
           '-output_format', 'json',
           '-show_streams',
           '-hide_banner',
           file,)

    # use ffprobe
    try:
        stdout = subprocess.check_output(cmd)
    except Exception as e:
        raise RuntimeError(f'Failed to run ffprobe on {file}') from e
    try:
        data = json.loads(stdout.decode())
        streams: list[dict[str, Any]] = data['streams']
    except Exception as e:
        raise ValueError(f'Failed to extract streams info for {file}') from e

    for s in streams:
        # try two ways to find duration info
        try:
            dur = s.get('duration')
            if dur:
                return float(dur)
        except Exception as e:
            raise ValueError(f'Failed to parse duration value for {file}') from e
    else:
        raise ValueError(f'No available duration value for {file}')


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
