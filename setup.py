#!/usr/bin/env python

from setuptools import setup, find_packages


from broker.version import version


def parse_requirements(filename):
    with open(filename, "r") as f:
        for line in f:
            if line and line[:2] not in ("#", "-e"):
                yield line.strip()


setup(
    name="broker",
    version=version,
    description="OpenKnot Broker",
    long_description=open("README.rst", "r").read(),
    author="James Mills",
    author_email="James Mills, prologic at shortcircuit dot net dot au",
    url="https://github.com/openknot/broker",
    download_url="https://github.com/openknot/broker/archive/master.zip",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
    ],
    license="TBA",
    keywords="openknot broker",
    platforms="POSIX",
    packages=find_packages("."),
    install_requires=list(parse_requirements("requirements.txt")),
    entry_points={
        "console_scripts": [
            "broker=broker.main:main"
        ]
    },
    zip_safe=True
)
