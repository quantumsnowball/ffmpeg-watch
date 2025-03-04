import sys
import traceback
from pathlib import Path

from ffmpeg_watch.default import run_ffmpeg_default
from ffmpeg_watch.utils import get_video_duration, hms, opt_val_of
from ffmpeg_watch.watch import run_ffmpeg_watch


def main() -> None:
    # verify args
    args = sys.argv[1:]

    # support only one -i flag
    # if args.count('-i') != 1:
    #     return run_ffmpeg_default(args)

    # count time opts
    ss = args.count('-ss')
    to = args.count('-to')
    t = args.count('-t')

    # any invalid time flag count will go to default
    if any(count > 1 for count in (ss, to, t)):
        return run_ffmpeg_default(args)

    # below are supported cases
    try:
        if t == 1:
            # dur=t
            dur = int(hms(opt_val_of('-t', args)))
        elif to == 1:
            # dur=to or to-ss
            dur = int(hms(opt_val_of('-to', args)))
            if ss == 1:
                dur -= int(hms(opt_val_of('-ss', args)))
        else:
            # dur=full or full-ss
            dur = get_video_duration(Path(opt_val_of('-i', args)))
            if ss == 1:
                dur -= int(hms(opt_val_of('-ss', args)))

        # run ffmpeg-watch
        return run_ffmpeg_watch(args, duration=dur)

    # on exception fall back to default
    except Exception:
        traceback.print_exc()
        if input(f'Retry with ffmpeg default? y/[N] ').lower() == 'y':
            return run_ffmpeg_default(args)
        return
