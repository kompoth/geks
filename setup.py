import os

from setuptools import Extension, setup
import numpy

try:
    from Cython.Build import cythonize
    HAS_CYTHON = True
except ImportError:
    HAS_CYTHON = False

USE_CYTHON = bool(int(os.getenv("USE_CYTHON", 0)))

if USE_CYTHON:
    src_file = os.path.join("geks", "cython", "fill_sinks.pyx")
else:
    src_file = os.path.join("geks", "cython", "fill_sinks.c")
    if not os.path.exists(src_file):
        src_file = os.path.join("geks", "cython", "fill_sinks.pyx")
        USE_CYTHON = True

if USE_CYTHON and not HAS_CYTHON:
    raise ImportError("No module named 'Cython'")

extensions = [Extension("geks.cython.fill_sinks", [src_file])]

if USE_CYTHON:
    extensions = cythonize(
        extensions, compiler_directives={"language_level": 3}
    )

setup(
    ext_modules=extensions,
    include_dirs=[numpy.get_include()],
)
