from setuptools import setup
from setuptools import find_packages

long_description= """
# jhutils
"""

required = []

setup(
    name="jhutils",
    version="0.0.1",
    description="Things I use all of the time.",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/jdchart/jh-py-utils",
    install_requires=required,
    packages=find_packages()
)