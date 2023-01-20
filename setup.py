from setuptools import setup, find_packages


VERSION = "0.0.11"

DESCRIPTION = "Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes"
LONG_DESCRIPTION = ""

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="whitebox-sdk",
    version=VERSION,
    author="Squaredev",
    author_email="hello@squaredev.io",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "model monitoring", "whitebox", "mlops"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
