# Geks

<p align="center">
    <a href="https://pypi.org/project/geks" target="_blank">
        <img src="https://img.shields.io/pypi/v/geks" alt="Package version">
    </a>
    <a href="https://pypi.org/project/geks" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/geks.svg" alt="Supported Python versions">
    </a> 
    <a href='https://coveralls.io/github/kompoth/geks?branch=main'>
        <img src='https://coveralls.io/repos/github/kompoth/geks/badge.svg?branch=main&kill_cache=1' alt='Coverage Status' />
    </a>
</p>
<p align="center">
    <img src="https://raw.githubusercontent.com/kompoth/geks/main/img/example.png" width="400">
</p>

Geks is a Python toolkit for generating geographical maps in a hexagonal lattice.

## Installation

To install latest version from PyPI:
```bash
pip install geks[mpl]
```
Suffix `mpl` means that Geks will be installed with `matplotlib` that powers a
testing front-end.

To install development version from GitHub (preferably in a virtual environment):
```bash
git clone https://github.com/kompoth/geks.git
make install-mpl
```
See other build and install commands in `Makefile`.

## Credits

- [Red Blob Games blog](https://www.redblobgames.com/)
- [Martin O'Leary article](https://mewo2.com/notes/terrain/)
- [Altitude generation for hexagonal maps](https://github.com/generesque/hexmap)
- [Planchon-Darboux method](https://www.researchgate.net/publication/240407597_A_fast_simple_and_versatile_algorithm_to_fill_the_depressions_of_digital_elevation_models)
