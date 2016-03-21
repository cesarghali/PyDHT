from setuptools import setup, find_packages
from pydht import version

setup(
    name="pydht",
    version=version,
    description="Pydht is a python implementation of a distributed hash table..",
    author="Cesar Ghali",
    author_email="cesarghali.p@gmail.com",
    license="GNU License",
    url="http://github.com/cesarghali/Pydht",
    packages=find_packages()
)
