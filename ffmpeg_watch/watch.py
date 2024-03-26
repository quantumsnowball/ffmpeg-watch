import sys
from subprocess import PIPE, Popen
from typing import Sequence

from tqdm import tqdm


def run_ffmpeg_watch(args: Sequence[str]) -> None:
    '''
    If ffmpeg-watch can calculate the necessary element to display a
    progress bar, this wrapper function will be triggered. It capture the
    stdout of ffmpeg process, and try to update the tqdm progress bar.
    '''
    # create basic ffmpeg command
    cmd = ['ffmpeg']
    cmd += args

    # additional options necessary for progress calc
    cmd[1:1] = ['-progress', 'pipe:1']
    cmd[1:1] = ['-stats_period', '0.1']

    # run ffmpeg in new process and wait
    proc = Popen(cmd, stdout=PIPE)
    proc.wait()

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

    # retain the same return code and exit
    sys.exit(proc.returncode)
