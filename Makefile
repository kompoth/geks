.PHONY: build build_ext dist redist install install-mpl clean uninstall

build:
	USE_CYTHON=1 python setup.py build

build_ext:
	USE_CYTHON=1 python setup.py build_ext --inplace

dist:
	USE_CYTHON=1 python setup.py sdist

redist: clean dist

install:
	USE_CYTHON=1 pip install .

install-mpl:
	USE_CYTHON=1 pip install .[mpl]

test: build_ext
	pytest

clean:
	rm -rf build dist 
	rm -rf geks/cython/*.c
	rm -rf geks/cython/*.so
	find . -name __pycache__ -exec rm -r {} +
	find . -name *.egg-info -exec rm -r {} +

uninstall:
	pip uninstall geks 
