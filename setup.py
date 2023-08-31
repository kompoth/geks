import os

from setuptools import Extension, setup
import numpy

USE_CYTHON = bool(int(os.getenv("USE_CYTHON", 0)))
if USE_CYTHON:
    try:
        from Cython.Build import cythonize
    except ImportError:
        if USE_CYTHON:
            raise

if USE_CYTHON:
    src_file = os.path.join("geks", "cython", "fill_sinks.pyx")
else:
    src_file = os.path.join("geks", "cython", "fill_sinks.c")

extensions = [Extension("geks.cython.fill_sinks", [src_file])]

if USE_CYTHON:
    extensions = cythonize(
        extensions, compiler_directives={"language_level": 3}
    )

setup(
    ext_modules=extensions,
    include_dirs=[numpy.get_include()],
)
