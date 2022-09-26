# setup.py template from Certipy @ly4k - https://github.com/ly4k/Certipy
from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="criminalip-python",
    version="0.0.1",
    license="MIT",
    author="choi",
    url="https://github.com/ChoiSG/criminalip-python",
    long_description=readme,
    install_requires=[
	    "Click",
	    "requests",
	    "aiohttp",
	    "asyncio",
	    "rich",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["cip=cip.__main__:main"],
    },
    description="Unofficial python CLI for CriminalIP.io from AI Spera",
)