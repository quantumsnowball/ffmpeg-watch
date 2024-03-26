from unittest.mock import ANY, patch

import pytest
from pytest_console_scripts import ScriptRunner


def test_main(script_runner: ScriptRunner):
    # just run ffmpeg or ffmpeg-watch with no args will return 1
    r1 = script_runner.run('ffmpeg', shell=True)
    r2 = script_runner.run('ffmpeg-watch', shell=True)
    assert r1.returncode == r2.returncode == 1


def test_multiple_i_flag(script_runner: ScriptRunner):
    with patch('ffmpeg_watch.cli.run_ffmpeg_default') as mock_fn:
        script_runner.run(['ffmpeg-watch', '-i', 'input1.mp4', '-i', 'input2.mp4', 'output.mp4'])
        mock_fn.assert_called_once_with(['-i', 'input1.mp4', '-i', 'input2.mp4', 'output.mp4'])


@pytest.mark.parametrize('ss, to, t, supported', [
    (0, 0, 1, True),
    (0, 1, 1, True),
    (1, 0, 1, True),
    (1, 1, 1, True),
    (0, 1, 0, True),
    (1, 1, 0, True),
    (0, 0, 0, True),
    (1, 0, 1, True),

    (2, 0, 1, False),
    (0, 2, 1, False),
    (0, 0, 2, False),
    (3, 0, 2, False),
    (0, 2, 2, False),
])
def test_time_opts(script_runner: ScriptRunner,
                   ss: int, to: int, t: int, supported: bool):
    '''
    ss to  t  solution
     0  0  1  dur=t
     0  1  1  dur=t(override to)
     1  0  1  dur=t
     1  1  1  dur=t(override to)
     0  1  0  dur=to
     1  1  0  dur=to-ss
     0  0  0  dur=full
     1  0  0  dur=full-ss
    '''
    command = ['ffmpeg-watch']
    args = ['-i', 'input.mp4']
    for _ in range(ss):
        args += ['-ss', '01:23:45']
    for _ in range(to):
        args += ['-to', '01:23:45']
    for _ in range(t):
        args += ['-t', '01:23:45']
    args += ['output.mp4']

    if supported:
        with (patch(f'ffmpeg_watch.cli.run_ffmpeg_watch') as do,
              patch(f'ffmpeg_watch.cli.run_ffmpeg_default') as dont):
            script_runner.run(command + args)
            do.assert_called_once_with(args, duration=ANY)
            dont.assert_not_called()
    else:
        with (patch(f'ffmpeg_watch.cli.run_ffmpeg_default') as do,
              patch(f'ffmpeg_watch.cli.run_ffmpeg_watch') as dont):
            script_runner.run(command + args)
            do.assert_called_once_with(args)
            dont.assert_not_called()
