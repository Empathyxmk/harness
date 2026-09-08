#!/bin/bash
set -e

echo "Setting up Python environment..."
pip install -r requirements.txt

echo "Compiling C examples for Python tests..."
# Compile examples used by tests, placing them in examples_c_bin
# Note: These compilation commands are derived from the source run_public_tests.sh and typical C project structures.
# They link necessary argtable3 source files.

# Ensure argtable3.h is visible, usually by including src/ in include paths
C_INCLUDE_PATH=$C_INCLUDE_PATH:./src

# Compile echo
echo "Compiling examples/echo.c..."
gcc -I./src -o examples_c_bin/echo examples/echo.c src/argtable3.c src/arg_utils.c src/arg_lit.c src/arg_str.c src/arg_end.c src/arg_dstr.c -lm

# Compile testargtable3
echo "Compiling examples/testargtable3.c..."
gcc -I./src -o examples_c_bin/testargtable3 examples/testargtable3.c src/argtable3.c src/arg_utils.c src/arg_lit.c src/arg_int.c src/arg_file.c src/arg_end.c src/arg_dstr.c -lm

# Compile mv (assuming it uses a subset of argtable3 features)
echo "Compiling examples/mv.c..."
gcc -I./src -o examples_c_bin/mv examples/mv.c src/argtable3.c src/arg_utils.c src/arg_lit.c src/arg_end.c src/arg_str.c src/arg_dstr.c -lm

# Compile myprog (assuming it uses a subset of argtable3 features)
echo "Compiling examples/myprog.c..."
gcc -I./src -o examples_c_bin/myprog examples/myprog.c src/argtable3.c src/arg_utils.c src/arg_lit.c src/arg_int.c src/arg_file.c src/arg_end.c src/arg_dstr.c -lm

# Compile multisyntax (assuming it uses a subset of argtable3 features)
echo "Compiling examples/multisyntax.c..."
gcc -I./src -o examples_c_bin/multisyntax examples/multisyntax.c src/argtable3.c src/arg_utils.c src/arg_lit.c src/arg_int.c src/arg_file.c src/arg_str.c src/arg_cmd.c src/arg_end.c src/arg_dstr.c -lm


echo "Running all Python tests..."
pytest

echo "All tests executed successfully!"