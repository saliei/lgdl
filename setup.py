from setuptools import setup

setup(
        name = "lgdl",
        version = "0.1.0",
        description = "Command Line Interface for Library Genesis.",
        long_description = "file: README.md",
        long_description_content_type = "text/markdown",
        url = "https://github.com/saliei/lgdl",
        author = "Saeid Aliei",
        author_email = "saeidaliei2019@pm.me",
        licence = "Apache-2.0",
        packages = ["lgdl"],
        install_requires = ["beautifulsoup4", "tqdm"],

        classifiers = [
            "Development Status :: 1 - Planning",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            ],
    )
