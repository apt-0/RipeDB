[![Downloads](https://static.pepy.tech/badge/ripedb)](https://pepy.tech/project/ripedb)

# RipeDB
<p align="center">
  <img src="https://github.com/apt-0/RipeDB/blob/main/assets/RipeDB_Image.jpg" width="300" height="300">
</p>

RipeDB is a Python tool designed to facilitate the search and analysis of internet domain data through the RIPE DATABASE. This project allows users to obtain detailed information about domains and their IP assignments.

## Features

- Search for domain information using customizable parameters.
- Analysis of collected data and generation of xlsx reports.
- Simple and intuitive user interface.

## Prerequisites

Before you begin, make sure you have Python 3.x installed on your system. RipeDB depends on some external packages, which are listed in the requirements.txt file.

## Installation

### Stable Version
RipeDB can be easily installed via pip. This method is recommended for most users as it automatically manages all project dependencies.

To install RipeDB, run the following command:

```bash
pip install ripedb
```

### Latest Version
If you want the Stable Version use this methods:

#### PIP
```bash
git clone https://github.com/apt-0/RipeDB
cd RipeDB
pip install .
```
If you want the Latest Version use this methods:

#### Python
```bash
git clone https://github.com/apt-0/RipeDB
cd RipeDB
python -m ripedb.main
```

## Usage
To start RipeDB, run the following command:
```bash
ripedb
```
or

```bash
ripedb -q <Search-Parameter>
```
If you want to edit the result you have to enter in editing-mode

```bash
ripedb -em
```
or 

```bash
ripedb -q <Search-Parameter> -em
```

## License
Distributed under the MIT License. See LICENSE for more information.

## Contacts
APT-0  - cryptovortex@outlook.com

## Contributors
[![Contributors](https://contrib.rocks/image?repo=apt-0/RipeDB)](https://github.com/apt-0/RipeDB/graphs/contributors)