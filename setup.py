from setuptools import setup, find_packages

setup(
    name="RipeDB",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pandas', 
    ],
    entry_points={
        'console_scripts': [
            'ripedb=ripedb.main:main',  # Cambia 'main:main' con il punto d'ingresso appropriato
        ],
    },
    author="APT-0-Blog",
    author_email="tuaemail@example.com",
    description="Uno strumento per effettuare query e analisi su RipeDB",
    keywords="ripe ripedb",
    url="URL del progetto", 
)
