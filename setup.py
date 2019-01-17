from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyfnork',
    version='0.0.1',
    description='Python Distribution Utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Erik Hartwig',
    author_email='erik.hartwig@gmail.com',
    url='https://github.com/fnork/pyfnork',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
