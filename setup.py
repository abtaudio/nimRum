from setuptools import setup


def getReadme():
    with open("README.md") as f:
        return f.read()


def getReqs():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="nimRum",
    description="Nimble Rumble, a library to play wireless(WiFi) sound in perfect synch, for private use and evaluation",
    long_description=getReadme(),
    long_description_content_type='text/markdown',
    keywords="abtaudio about time audio wireless sound synchronization",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Embedded Systems",
    ],
    version="0.1.dev1",
    license="AbtAudio",
    author="AbtAudio AB",
    author_email="evaluate@abtaudio.tech",
    url="https://github.com/abtaudio/nimRum",
    python_requires=">=3",
    install_requires=getReqs(),
    scripts=["bin/runNimRumRx.py", "bin/runNimRumTx.py", "bin/runNimRumForever.sh"],
    zip_safe=False,
    include_package_data=True,
    packages=["nimRum"],
    package_dir={"nimRum": "nimRum"},
    package_data={"nimRum": ["*.so", "txConfig.yaml", "gitStatus.txt"]},
)
