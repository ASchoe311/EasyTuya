import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / "license.txt").read_text()

# This call to setup() does all the work
setup(
    name="TuyaPy",
    version="0.1",
    description="Interact with devices connected to the Tuya IOT platform through Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ASchoe311/TuyaPy",
    author="Adam Schoenfeld",
    author_email="aschoe@umich.edu",
    license=LICENSE,
    classifiers=[
        "License :: OSI Approved :: GNU GPLv3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TuyaPy", "TuyaPy.devices"],
    include_package_data=True,
    install_requires=["pycryptodome"]
)