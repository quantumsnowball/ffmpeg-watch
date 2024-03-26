import sys

from ffmpeg_watch.default import run_default_ffmpeg
from ffmpeg_watch.watch import run_ffmpeg_watch

'''
ss to  t case
 0  0  1 bar dur=t
 0  1  1 def dur=t(override to)
 1  0  1 bar dur=t
 1  1  1 def dur=t(override to)
 0  1  0 bar dur=to
 1  1  0 bar dur=to-ss
 0  0  0 bar dur=full
 1  0  0 bar dur=full-ss
'''


def main() -> None:
    # verify args
    args = sys.argv[1:]

    # support only one -i flag
    if args.count('-i') != 1:
        return run_default_ffmpeg(args)

    # count time opts
    ss = args.count('-ss')
    to = args.count('-to')
    t = args.count('-t')

    # any invalid time flag count will go to default
    if any(0 <= count <= 1 for count in (ss, to, t)):
        return run_default_ffmpeg(args)

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
