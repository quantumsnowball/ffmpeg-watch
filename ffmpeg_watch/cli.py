import sys

from ffmpeg_watch.default import run_ffmpeg_default
from ffmpeg_watch.utils import hms, opt_val_of
from ffmpeg_watch.watch import run_ffmpeg_watch


def main() -> None:
    # verify args
    args = sys.argv[1:]

    # support only one -i flag
    if args.count('-i') != 1:
        return run_ffmpeg_default(args)

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
            secs = int(hms(opt_val_of('-t', args)))
        elif to == 1:
            # dur=to or to-ss
            secs = int(hms(opt_val_of('-to', args)))
            if ss == 1:
                secs -= int(hms(opt_val_of('-ss', args)))
        else:
            # dur=full or full-ss
            secs = 1000  # TODO
            if ss == 1:
                secs -= int(hms(opt_val_of('-ss', args)))

        # run ffmpeg-watch
        return run_ffmpeg_watch(args, duration=secs)

    # on exception fall back to default
    except Exception as e:
        if input(f'{e}, retry with ffmpeg default? y/[N] ').lower() == 'y':
            return run_ffmpeg_default(args)
        return
