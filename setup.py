import setuptools


description = (
    "Whitebox is an open source E2E ML monitoring platform with edge capabilities"
)
requirements = [i.strip() for i in open("requirements.txt").readlines()]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whitebox",  # This is the name of the package
    version="0.0.1",  # The initial release version
    author="Squaredev",  # Full name of the author
    description=description,
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires=">=3.6",  # Minimum version requirement of the package
    py_modules=["whitebox"],  # Name of the python package
    # package_dir={"": "src/sdk"},  # Directory of the source code of the package
    install_requires=requirements,
)
