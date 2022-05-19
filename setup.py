import pathlib
from setuptools import setup, find_packages

# The directory containing this file
ROOT_DIR = pathlib.Path(__file__).parent

# The text of the README file
README = (ROOT_DIR / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lpminimk3",
    version="0.5.0",
    description="Python API for the Novation Launchpad Mini MK3",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/obeezzy/lpminimk3",
    author="Chronic Coder",
    author_email="efeoghene.obebeduo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["python-rtmidi", "jsonschema", "websockets"],
)
