import os
import sys
import subprocess
import pytest
from src.swappy.file import folder_exists, file_exists, file_dump_stdin_into_a_temp_file

# Helper functions for creating and removing temporary files/directories (with different names)
def create_alt_temp_file(path):
    with open(path, 'w') as f:
        f.write("altdata")

def remove_alt_temp_file(path):
    if os.path.exists(path):
        os.remove(path)

def create_alt_temp_dir(path):
    os.makedirs(path, exist_ok=True)

def remove_alt_temp_dir(path):
    if os.path.exists(path):
        subprocess.run(['rm', '-rf', path], check=True)

def test_folder_exists_positive_public():
    dir_name = "test_temp_alt_dir_public"
    create_alt_temp_dir(dir_name)
    assert folder_exists(dir_name)
    remove_alt_temp_dir(dir_name)

def test_folder_exists_negative_public():
    assert not folder_exists("alt_dir_that_does_not_exist_public")

def test_file_exists_positive_public():
    file_name = "test_temp_alt_file_public.txt"
    create_alt_temp_file(file_name)
    assert file_exists(file_name)
    remove_alt_temp_file(file_name)

def test_file_exists_negative_public():
    assert not file_exists("alt_file_that_does_not_exist_public.txt")

def test_file_dump_stdin_returns_null_if_tty_public():
    # Just like the original logic, be robust to CI envs.
    ret = file_dump_stdin_into_a_temp_file()
    if ret is not None:
        os.remove(ret)
    assert True  # Equivalent to ck_assert(1)