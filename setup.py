from setuptools import setup, find_packages

setup(
    name="RipeDB",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pandas', 
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'ripedb=main:main', 
        ],
    },
    author="APT-0-Blog",
    author_email="cryptovortex@outlook.com",
    description="Uno strumento per effettuare query e analisi su RipeDB",
    keywords="ripe ripedb",
    url="https://github.com/apt-0/RipeDB", 
)
