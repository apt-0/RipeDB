from setuptools import setup, find_packages

with open("README.md", "r") as fh: 
    long_description = fh.read() 

setup(
    name="RipeDB",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pandas', 
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'ripedb=ripedb.main:main', 
        ],
    },
    long_description=long_description, 
    long_description_content_type="text/markdown",
    author="APT-0-Blog",
    author_email="cryptovortex@outlook.com",
    description="Uno strumento per effettuare query e analisi su RipeDB",
    keywords="ripe ripedb",
    url="https://github.com/apt-0/RipeDB", 
)
