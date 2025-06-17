"""
Setup script for AB Race Translator package

Converted from C++ ABRace system to Python package for processing
racing bet messages in LOGAB format.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AB Race Translator - Convert C++ racing message processing to Python"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="ab-race-translator",
    version="1.0.0",
    author="Converted from C++ ABRace",
    author_email="developer@company.com",
    description="Python package for translating AB Racing messages from C++ LOGAB format",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ab-race-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'isort>=5.12.0',
        ],
        'build': [
            'build>=0.10.0',
            'twine>=4.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'ab-race-translate=ab_race_translator.example_usage:main',
        ],
    },
    package_data={
        'ab_race_translator': [
            '*.py',
            'py.typed',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        'racing', 'betting', 'message-translator', 'logab', 'c++', 'conversion',
        'binary-parser', 'financial', 'horse-racing', 'data-processing'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/your-org/ab-race-translator/issues',
        'Source': 'https://github.com/your-org/ab-race-translator',
        'Documentation': 'https://github.com/your-org/ab-race-translator/blob/main/README.md',
    },
)
