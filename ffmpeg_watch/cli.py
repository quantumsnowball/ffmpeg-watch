import sys
from subprocess import Popen


def main() -> None:
    # verify args
    args = sys.argv[1:]

    # create ffmpeg command
    cmd = ['ffmpeg']
    cmd += args
    cmd[1:1] = ['-progress', 'pipe:1']
    cmd[1:1] = ['-stats_period', '0.1']

    # run ffmpeg in process
    proc = Popen(cmd)
    proc.wait()

    # decide if capable to display progress bar or not
    # read through PIPE and display progress bar

    # retain return code
    sys.exit(proc.returncode)
