from setuptools import setup
import sys, os

setup(
        name = "lgdl",
        version = "0.1.0",
        description = "Command Line Interface for Library Genesis.",
        long_description = "file: README.md",
        long_description_content_type = "text/markdown",
        url = "https://github.com/saliei/lgdl",
        author = "Saeid Aliei",
        author_email = "saeidaliei2019@gmail.com",
        license = "Apache-2.0",
        packages = ["lgdl"],
        install_requires = ["beautifulsoup4", "tqdm"],
        entry_points = {"console_scripts": ["lgdl = bin.lgdl:main"]},
        # data_files = [(os.path.expanduser("~/.config"), ["lgdl/lgdlrc"])],
        package_data = {"lgdl": ["config/lgdlrc"]},

        classifiers = [
            "Development Status :: 1 - Planning",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            ],
    )

