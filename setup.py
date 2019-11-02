from distutils.core import setup

from pkg_resources import parse_requirements
from setuptools import find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

with open("requirements-dev.txt") as f:
    REQUIREMENTS_DEV = [str(req) for req in parse_requirements(f.read())]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="recogn-img",
    version="0.0.2",
    description="Library for simple object recognition in images using YOLO model",
    author="Mateusz Korzeniowski",
    author_email="emkor93@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emkor/recogn-img",
    packages=find_packages(exclude=("recogn_img.test", "recogn_img.test.*")),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_DEV,
    extras_require={
        "dev": REQUIREMENTS_DEV
    },
    entry_points={
        "console_scripts": [
            "recogn-img = recogn_img.recogn_main:cli_main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities"
    ],
)
