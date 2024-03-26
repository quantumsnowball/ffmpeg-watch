import sys
from subprocess import PIPE, Popen
from typing import Sequence

from tqdm import tqdm

from ffmpeg_watch.default import run_default_ffmpeg


def run_tqdm() -> Popen:
    print('run_tqdm()')
    sys.exit(proc.returncode)


def main() -> None:
    # verify args
    args = sys.argv[1:]

    # support only one -i flag, otherwise, just run default ffmpeg
    if args.count('-i') != 1:
        return run_default_ffmpeg(args)

    # if only -t flag or -to flag, already know the duration
    ss_opt_count = args.count('-ss')
    to_opt_count = args.count('-to')
    t_opt_count = args.count('-t')
    breakpoint()
    # if only the -ss flag, need to find our the length of stream to calc

    # create ffmpeg command
    cmd = ['ffmpeg']
    cmd += args
    cmd[1:1] = ['-progress', 'pipe:1']
    cmd[1:1] = ['-stats_period', '0.1']

    # run ffmpeg in process
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    # read through PIPE and display progress bar
    if proc.stdout is not None:
        # display a progress bar
        with tqdm(total=1000) as pbar:
            for line_b in proc.stdout:
                line = line_b.decode().strip()
                # track ffmpeg rendering speed
                if line.startswith('speed='):
                    speed_text = line.split('=', maxsplit=1)[1]
                    speed = float(speed_text.replace('x', ''))
                    progress = speed * 0.1
                    # pbar(progress)
                    pbar.update(1)

            # finish bar to 100%
            pbar.update(1000)
    proc.wait()

    # decide if capable to display progress bar or not

    # retain return code
    sys.exit(proc.returncode)
