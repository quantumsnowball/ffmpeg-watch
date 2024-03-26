from unittest.mock import patch

import pytest
from pytest_console_scripts import ScriptRunner


def test_main(script_runner: ScriptRunner):
    # just run ffmpeg or ffmpeg-watch with no args will return 1
    r1 = script_runner.run('ffmpeg', shell=True)
    r2 = script_runner.run('ffmpeg-watch', shell=True)
    assert r1.returncode == r2.returncode == 1


def test_multiple_i_flag(script_runner: ScriptRunner):
    '''
    ss to  t target
     0  0  1 bar dur=t
     0  1  1 def dur=t(override to)
     1  0  1 bar dur=t
     1  1  1 def dur=t(override to)
     0  1  0 bar dur=to
     1  1  0 bar dur=to-ss
     0  0  0 bar dur=full
     1  0  0 bar dur=full-ss
    '''
    with patch('ffmpeg_watch.cli.run_default_ffmpeg') as mock_fn:
        script_runner.run(['ffmpeg-watch', '-i', 'input1.mp4', '-i', 'input2.mp4', 'output.mp4'])
        mock_fn.assert_called_once_with(['-i', 'input1.mp4', '-i', 'input2.mp4', 'output.mp4'])
