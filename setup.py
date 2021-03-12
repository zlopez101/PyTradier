from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="PyTradier",
    version="0.1.0",
    author="Zach",
    description="Python wrapper for Tradier API",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
