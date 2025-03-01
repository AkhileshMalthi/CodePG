from setuptools import setup, find_packages

setup(
    name="codepg",
    version="0.1.0",
    description="A CLI tool for creating organized coding playground files",
    author="CodePG Developer",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "codepg=codepg.app:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
