from re import match as re_match
from setuptools import setup, find_packages

setup(
    name='bountysnakeai',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[x for x in open('requirements.txt').read().splitlines() if re_match('^[a-zA-Z]', x)],
)

