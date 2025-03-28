import sys
import traceback

from ffmpeg_watch.default import prompt_ffmpeg_default
from ffmpeg_watch.utils import (FFmpegInputPath, get_video_duration, hms,
                                opt_val_of)
from ffmpeg_watch.watch import run_ffmpeg_watch


def main() -> None:
    # verify args
    args = sys.argv[1:]

    # count related opts
    # i = input file, ss = start time, to = end time, t = duration
    i = args.count('-i')
    ss = args.count('-ss')
    to = args.count('-to')
    t = args.count('-t')
    # only support single -i options
    if i == 0:
        print('ffmpeg-watch requires at least one -i input_file to calculate processing time')
        return prompt_ffmpeg_default(args)
    # any invalid time flag count will go to default
    if any(count > 1 for count in (ss, to, t)):
        print('ffmpeg-watch does not support multiple -t, -ss, -to options')
        return prompt_ffmpeg_default(args)

    # ensure input file path exists or is a valid ffmpeg supported printf pattern
    try:
        input_file = FFmpegInputPath(opt_val_of('-i', args))
        assert input_file.is_file() or input_file.is_printf_pattern()
    except Exception:
        print('ffmpeg-watch requires a valid -i input_file file path or pattern')
        return prompt_ffmpeg_default(args)

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
            dur = get_video_duration(input_file)
            if ss == 1:
                dur -= int(hms(opt_val_of('-ss', args)))
    # catch simple value error first
    except ValueError as e:
        print(e)
        return prompt_ffmpeg_default(args)
    # on exception fall back to default
    except Exception:
        print('ffmpeg-watch failed to calculate processing time due to the following exceptions:\n')
        traceback.print_exc()
        return prompt_ffmpeg_default(args)
    # run ffmpeg-watch
    else:
        return run_ffmpeg_watch(args, duration=dur)
