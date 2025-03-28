import sys
from subprocess import PIPE, Popen
from typing import Sequence

# from tqdm import tqdm
from alive_progress import alive_bar


def run_ffmpeg_watch(args: Sequence[str],
                     duration: float) -> None:
    '''
    If ffmpeg-watch can calculate the necessary element to display a
    progress bar, this wrapper function will be triggered. It capture the
    stdout of ffmpeg process, and try to update the tqdm progress bar.
    '''
    STATS_PERIOD = 0.1

    # create basic ffmpeg command
    cmd = ['ffmpeg']
    cmd += args

    # additional options necessary for progress calc
    cmd[1:1] = ['-loglevel', 'fatal']
    cmd[1:1] = ['-progress', 'pipe:1']
    cmd[1:1] = ['-stats_period', str(STATS_PERIOD)]

    # run ffmpeg in new process and wait
    proc = Popen(cmd, stdout=PIPE)

    # read through PIPE and display progress bar
    if proc.stdout is not None:
        # block until first line in stdout is available
        # NOTE:
        # stderr may prompt for overwrite confirmation, before that
        # don't showing progress bar to keep the interface clean
        proc.stdout.readline()

        # display a progress bar
        with alive_bar(manual=True) as bar:
            pct = 0.0
            for line_b in proc.stdout:
                line = line_b.decode().strip()
                # track ffmpeg rendering speed
                if line.startswith('speed='):
                    speed_text = line.split('=', maxsplit=1)[1]
                    # calc and show speed
                    try:
                        speed = float(speed_text.replace('x', ''))
                    except ValueError:
                        continue
                    bar.text(speed_text)
                    # calc and show progress percentage
                    pct += round(speed * STATS_PERIOD) / duration
                    bar(min(pct, 1.0))

            # finish bar to 100%
            bar(1.0)
    proc.wait()

    # retain the same return code and exit
    sys.exit(proc.returncode)
