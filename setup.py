"""
Setup file for deeprdn
Refer to https://github.com/rodrigoazs/deeprdn
"""

from setuptools import setup
from setuptools import find_packages
from os import path


setup(
    name="deeprdn",
    packages=find_packages(exclude=["test"]),
    package_dir={"srlearn": "srlearn"},
    author="Rodrigo Azevedo Santos (rodrigoazs)",
    author_email="rodrigoazvsantos@gmail.com",
    description="A deep learning approach for SRL.",
    download_url="https://github.com/rodrigoazs/deeprdn",
    license="GPL-3.0",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="machine-learning-algorithms machine-learning statistical-learning pattern-classification artificial-intelligence",
    install_requires=["numpy", "srlearn", "pandas", "tensorflow"],
    extras_require={
        "tests": ["pytest"],
    },
)
