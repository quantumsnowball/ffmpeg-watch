import sys

from ffmpeg_watch.default import run_ffmpeg_default
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

    # if t flag, duration is know
    if t == 1:
        # dur=t
        return run_ffmpeg_watch(args)
    elif to == 1:
        # dur=to or to-ss
        return run_ffmpeg_watch(args)
    else:
        # dur=full or full-ss
        return run_ffmpeg_watch(args)
