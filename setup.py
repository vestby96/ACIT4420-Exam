from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ACIT4420",
    version="1.0.0",
    author="130",
    description="A Python package for the ACIT4420 exam",       # Short description
    long_description=long_description,                          # FUll description
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",                  # Python version
        "Operating System :: OS Independent",                   # OS independent
    ],
    python_requires=">=3.10",                                   # Minimum Python version required
    install_requires=[                                          # Required libraries and packages
        "networkx",
        "matplotlib",
        "geopy",
    ],
    entry_points={                                              # package entry points
        "console_scripts": [
            "tarjan-planner=package.tarjan_planner.main:main",  # Create CLI command tarjan-planner
            "file-organizer=package.file_organizer.main:main",  # Create CLI command file-organizer
        ],
    },
)