# olieigra
A project that parses IGRA2 formatted data. IGRA [Integrated Global Radiosonde Archive](https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive) is an online archive of weather balloon data.

## Problem
As a data scientist/data engineer, I want to read IGRA2 files as a stream with the minimum amount of pre-processing.

## Solution
Parse an IGRA2 file utilizing a series of callbacks. These callbacks are configured by the calling application. This provides for a separation of concerns. The calling application has complete control over the transformation and storage of the data.

IGRA2 files are typically downloaded as a zipped archives. The solution has the ability to scan for zip files in a folder. It will process IGRA2 files contained within zip files without expanding it locally.

## Project Structure
- /src/olieigra - Implementation code
- /dist - Packaged olieigra wheel file to be installed with pip
- /tests - Unit testing code (unittest)
- LICENSE - MIT License
- pyproject.toml - Configuration file for packaging
- README.md - This file
- sample_gph20s10k.py - A sample implementation using olieigra. It interpolates data over 20 levels.
- sample_qa.py - A very simple implementation using olieigra. It writes a very simple aggregate of data. 

## Installation
Dependencies:
- numpy
- pytest

### Option 1
[Download](https://github.com/olievortex/olieigra/releases) the .whl file from the latest release and install it using pip. (Replace the text 'version' below with the actual file version.)

    pip install /path/to/whl/olieigra-version-py3-none-any.whl

### Option 2 
Clone the repository and build your own package.

    cd /path/to/cloned/repository
    conda activate your_environment
    conda install build
    python -m build

A .whl file will be created in the /dist/ folder. Take this file and install as you would using Option 1 above.

## Usage and Documentation
[Please refer to the repository Wiki](https://github.com/olievortex/olieigra/wiki)

## Issue Tracking
[Please refer to the repository issue tracker](https://github.com/olievortex/olieigra/issues)

## Coding Style
Pylint should be used to assure code quality. The Python code should be formatted using Autopep8.
