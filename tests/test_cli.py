from pytest_console_scripts import ScriptRunner


def test_main(script_runner: ScriptRunner):
    # just run ffmpeg or ffmpeg-watch with no args will return 1
    r1 = script_runner.run('ffmpeg', shell=True)
    r2 = script_runner.run('ffmpeg-watch', shell=True)
    assert r1.returncode == r2.returncode == 1
