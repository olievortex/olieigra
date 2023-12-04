# olieigra
A project that parses IGRA2 formatted data. IGRA [Integrated Global Radiosonde Archive](https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive) is an online archive of weather balloon data.

## Problem
As a data scientist/data engineer, I want to read IGRA2 files as a stream with the minimum amount of pre-processing.

## Solution
Parse an IGRA2 file utilizing a series of callbacks. These callbacks are configured by the calling application. This provides for a separation of concerns. The calling application has complete control over the transformation and storage of the data.

## Project Structure
- /src/olieigra - Implementation code
- /dist - Packaged olieigra wheel file to be installed with pip
- /tests - Unit testing code (unittest)
- LICENSE - MIT License
- pyproject.toml - Configuration file for packaging
- README.md - This file

## Installation
Dependencies:
- numpy
- pytest

Download the most recent *.whl file from the /dist folder. Install using pip. Replace 'version' in the command below with the actual version of your download.

    pip install /path/to/whl/olieigra-version-py3-none-any.whl

## Usage and Documentation
[Please refer to the repository Wiki](https://github.com/olievortex/olieigra/wiki)

## Issue Tracking
[Please refer to the repository issue tracker](https://github.com/olievortex/olieigra/issues)

## Coding Style
Pylint should be used to assure code quality. The Python code should be formatted using Autopep8.
