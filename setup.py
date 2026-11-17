"""
Setup script for Skills08.
"""

from setuptools import setup, find_packages

setup(
    name="skills08",
    version="0.2.0",
    description="Local-First AI Agent Skill Distribution & Lifecycle Manager",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "skills08=skills08.cli:main",
        ],
    },
)
