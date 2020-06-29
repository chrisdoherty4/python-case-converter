from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="case-converter",
    version="1.0.1",
    url="https://github.com/chrisdoherty4/python-case-converter",
    packages=find_packages(exclude=["*_test.py"]),
    author="Chris Doherty",
    author_email="chris@chrisdoherty.io",
    description="A string case conversion package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["case", "convert", "converter", "string"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Programming Language :: Python :: 3",
    ],
)
