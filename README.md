# Geks

Geks is a toolkit for hexagonal mapmaking. 

<p align="center">
    <img src="https://raw.githubusercontent.com/kompoth/geks/main/img/example.png" width="600">
</p>

## Installation

Currently there is no PyPI package.

To install development version from GitHub (preferably in a virtual environment):
```bash
git clone https://github.com/kompoth/geks.git
make install-mpl
```
Suffix `mpl` means that Geks will be installed with `matplotlib` that powers a
testing front-end. See other build and install commands in `Makefile`.

## Credits

- [Red Blob Games blog](https://www.redblobgames.com/)
- [Martin O'Leary article](https://mewo2.com/notes/terrain/)
- [Altitude generation for hexagonal maps](https://github.com/generesque/hexmap)
- [Planchon-Darboux method](https://www.researchgate.net/publication/240407597_A_fast_simple_and_versatile_algorithm_to_fill_the_depressions_of_digital_elevation_models)
