from setuptools import setup, find_packages
import oclock

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='oclock',
    version=oclock.__version__,
    author='Olivier Vincent',
    author_email='olivier.vincent@univ-lyon1.fr',
    url='https://cameleon.univ-lyon1.fr/ovincent/oclock',
    description='Cancellable timer for constant duration loops',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'
)
