from unittest.mock import patch

import pytest
from pytest_console_scripts import ScriptRunner


def test_main(script_runner: ScriptRunner):
    # just run ffmpeg or ffmpeg-watch with no args will return 1
    r1 = script_runner.run('ffmpeg', shell=True)
    r2 = script_runner.run('ffmpeg-watch', shell=True)
    assert r1.returncode == r2.returncode == 1


def test_multiple_i_flag(script_runner: ScriptRunner):
    with patch('ffmpeg_watch.cli.run_default_ffmpeg') as mock_fn:
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

    (0, 2, 1, False),
])
def test_time_opts(script_runner: ScriptRunner, ss, to, t, supported):
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

    fns = ('run_ffmpeg_watch', 'run_default_ffmpeg')
    should_run, should_not_run = fns if supported else reversed(fns)

    with (patch(f'ffmpeg_watch.cli.{should_run}') as should_run_mock,
          patch(f'ffmpeg_watch.cli.{should_not_run}') as should_not_run_mock):
        script_runner.run(command + args)
        should_run_mock.assert_called_once_with(args)
        should_not_run_mock.assert_not_called()
