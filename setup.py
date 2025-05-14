from setuptools import setup, find_packages

setup(
    name="canort",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    author="Jiheng Hu",
    author_email="hjh18305@gmail.com",
    description="Canopy Microwave Radiative Transfer model",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jihenghu/canort",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 