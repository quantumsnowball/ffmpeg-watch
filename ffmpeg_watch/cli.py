import sys
from subprocess import Popen


def main() -> None:
    args = sys.argv[1:]
    cmd = ['ffmpeg'] + args
    proc = Popen(cmd)
    proc.wait()
    sys.exit(proc.returncode)
