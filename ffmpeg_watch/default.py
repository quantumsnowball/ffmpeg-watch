import sys
from subprocess import Popen
from typing import Sequence


def run_ffmpeg_default(args: Sequence[str]) -> None:
    '''
    This is just the default for most unsupport case
    If ffmpeg-watch is not confidence to perform its function,
    it will past all args to the default ffmpeg for handling
    '''
    # create the default command
    cmd = ['ffmpeg'] + list(args)

    # run ffmpeg in new process and wait
    proc = Popen(cmd)
    proc.wait()

    # retain the same return code and exit
    sys.exit(proc.returncode)


def prompt_ffmpeg_default(args: Sequence[str]) -> None:
    if input(f'\nRetry with ffmpeg default? y/[N] ').lower() == 'y':
        return run_ffmpeg_default(args)
    
