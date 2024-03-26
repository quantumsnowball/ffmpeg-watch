from setuptools import setup

setup(
    name='ffmpeg-watch',
    version='0.1.0',
    description='ffmpeg-watch - ffmpeg but easier to use',
    url='https://github.com/quantumsnowball/ffmpeg-watch',
    author='Quantum Snowball',
    author_email='quantum.snowball@gmail.com',
    license='MIT',
    packages=['ffmpeg_watch'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ffmpeg-watch=ffmpeg_watch.cli:main',
        ]
    }
)
