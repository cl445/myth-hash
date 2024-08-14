from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="myth-hash",
    version="0.1.0",
    author="Claas Flint",
    author_email="claas.flint@gmail.com",
    description="A tool for generating human-readable, multilingual fantasy character names based on input string hashes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myth_hash",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "myth-hash=myth_hash.cli:main",
        ],
    },
    package_data={
        "myth_hash": ["data/*.json"],
    },
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
