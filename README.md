[![Downloads](https://static.pepy.tech/badge/ripedb)](https://pepy.tech/project/ripedb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
If you want the Latest Version use this methods (Not all Parameter works):

#### PIP
```bash
git clone https://github.com/apt-0/RipeDB
cd RipeDB
pip install .
```
#### Python
```bash
git clone https://github.com/apt-0/RipeDB
cd RipeDB
python -m ripedb.main
```

## Usage
To start RipeDB, run the following command:
```bash
ripedb -h


····················································
:                                                  :
: 888 88e  ,e,                  888 88e   888 88b, :
: 888 888D  "  888 88e   ,e e,  888 888b  888 88P' :
: 888 88"  888 888 888b d88 88b 888 8888D 888 8K   :
: 888 b,   888 888 888P 888   , 888 888P  888 88b, :
: 888 88b, 888 888 88"   "YeeP" 888 88"   888 88P' :
:              888                                 :
:              888                                 :
:                                                  :
····················································

usage: main.py [-h] [-q QUERY] [-em] [-o OUTPUT] [-dns DNS] [command]

RipeDB: A tool for performing queries and analysis on RipeDB.

positional arguments:
  command               The command to execute (query, help).

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Query parameter
  -em, --editing-mode   Enable DNS resolution and editing mode
  -o OUTPUT, --output OUTPUT
                        Define output folder
  -dns DNS, -dns DNS    Perform DNS Lookup without edit the result
```
or

```bash
ripedb -q <Search-Parameter>
```
If you want to edit the result and perform DNS LOOKUP, you have to enter in editing-mode

```bash
ripedb -em
```
or 

```bash
ripedb -q <Search-Parameter> -em
```

For output the Search resuts or DNS Result (via editing mode) define -o parameter:
```bash
ripedb -q <Search-Parameter> -o <Output-Path>
```
You Can Define output parameter as follow:
- ripedb -o '.'
- ripedb -o 'PATH'

## License
Distributed under the MIT License. See LICENSE for more information.

## Contacts
APT-0  - cryptovortex@outlook.com

## Contributors
[![Contributors](https://contrib.rocks/image?repo=apt-0/RipeDB)](https://github.com/apt-0/RipeDB/graphs/contributors)