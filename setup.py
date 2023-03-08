"""John Deere API wrapper."""

from __future__ import annotations

import setuptools


DOCLINES = __doc__.split("\n")

REQUIREMENTS = [
    "requests<3.0,>=2.25.1",
    "aenum<4.0,>=3.1.11",
    "yarl<2.0,>=1.8.2",
]


setuptools.setup(
    name="johndeere",
    version="0.0.2",
    author="Arbyn Acosta",
    author_email="arbyn.acosta@gmail.com",
    # url="https://github.com/adw0rd/instagrapi",
    install_requires=REQUIREMENTS,
    keywords=[
        "john deere",
        "john-deere",
        "john deere api",
        "john-deere-api",
        "john deere client",
        "john-deere-client",
    ],
    description=DOCLINES[0],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
