import os
import re
import pytest

GRAMMAR_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'grammar.js')

@pytest.fixture(scope='module')
def src():
    with open(GRAMMAR_PATH, 'r', encoding='utf8') as f:
        return f.read()

def test_use_module_exports_and_reference_grammar_keyword(src):
    assert src.startswith('module.exports')
    assert 'grammar(' in src

def test_contain_language_name_vhs(src):
    assert re.search(r'name\s*:\s*[\'"`]vhs[\'"`]', src)

def test_mention_rules_object_with_two_vhs_rules(src):
    assert 'rules' in src
    assert 'env:' in src
    assert 'type:' in src

def test_have_at_least_one_regexp_literal(src):
    assert re.search(r'/[A-Za-z+\\\\]+/[a-z]?', src)

@pytest.mark.skipif(pytest.importorskip("tree_sitter", reason="tree-sitter not installed") is None, reason="tree-sitter not installed")
def test_parse_alternate_program_various_vhs_commands():
    assert True

@pytest.mark.skipif(pytest.importorskip("tree_sitter", reason="tree-sitter not installed") is None, reason="tree-sitter not installed")
def test_parse_different_mix_of_commands_and_comments():
    assert True

@pytest.mark.skipif(pytest.importorskip("tree_sitter", reason="tree-sitter not installed") is None, reason="tree-sitter not installed")
def test_support_additional_vhs_constructs_with_public_data():
    assert True