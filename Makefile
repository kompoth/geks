.PHONY: build dist redist install install-from-source clean uninstall

build:
	USE_CYTHON=1 python setup.py build

dist:
	USE_CYTHON=1 python setup.py sdist bdist_wheel

redist: clean dist

install:
	USE_CYTHON=1 pip install .

clean:
	rm -rf build dist 
	rm -rf geks/cython/*.c
	find . -name __pycache__ -exec rm -r {} +
	find . -name *.egg-info -exec rm -r {} +

uninstall:
	pip uninstall geks 
