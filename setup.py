from setuptools import setup, find_packages

setup(
    name="Case Converter",
    version="0.1",
    packages=find_packages(exclude=["*_test.py"]),
    author="Chris Doherty",
    author_email="chris@chrisdoherty.io",
    description="Case conversion package for strings.",
    keywords="case convert converter string"
)