from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Define the extension module
extensions = [
    Extension(
        "neuronet",                 # Name of the module
        sources=[
            "cython/neuronet.pyx",  # Cython source
            "src/GrafoDisperso.cpp" # C++ source
        ],
        include_dirs=["include"],   # Include directories
        language="c++",             # Use C++ compiler
        extra_compile_args=["-std=c++11", "-O3"], # Optimization flags
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions),
)
