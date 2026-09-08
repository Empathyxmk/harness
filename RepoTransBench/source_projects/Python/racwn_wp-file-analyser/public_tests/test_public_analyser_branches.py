import sys
import os
import pytest

# Ensure the wpanalyser package is on the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import wpanalyser.analyser as analyser


def test_different_branch_count():
    # Different from default, using public different data
    file_content = "<?php\nif(1){echo 'a';}else{echo 'b';}\nif(2){echo 'c';}\n"
    result = analyser.count_branches(file_content)
    # We expect 2 if-branches (matching core logic in a distinct way from original tests)
    assert result == 2

def test_switch_case_branch():
    file_content = "<?php\nswitch($var){case 2: break; case 3: break; default: break;}\n"
    result = analyser.count_branches(file_content)
    assert result == 1  # A switch counts as a single branch

def test_multiple_elseif_branch():
    file_content = "<?php\nif($a==2){echo 2;}elseif($a==3){echo 3;}elseif($a==4){echo 4;}\n"
    result = analyser.count_branches(file_content)
    assert result == 1  # Still one if-elseif-else chain per logic

def test_nested_if_else_branch():
    file_content = "<?php\nif($a){if($b){echo 1;}else{echo 2;}}\n"
    result = analyser.count_branches(file_content)
    assert result == 2  # Outer and inner ifs

def test_try_catch_count():
    file_content = "<?php\ntry{ risky(); } catch(Exception $e) {} catch(Error $e) {}\n"
    result = analyser.count_branches(file_content)
    assert result == 1  # Try-catch should be counted as one branch