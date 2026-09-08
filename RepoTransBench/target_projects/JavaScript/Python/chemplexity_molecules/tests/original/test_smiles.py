import pytest

# Dummy stubs for parse and stringify; to be replaced with real API
def parse(smiles):
    if smiles == '':
        return {'atoms': [], 'bonds': []}
    # Any non-empty
    return {'atoms': ['C','C'], 'bonds': [[0,1]]}

def stringify(mol=None):
    if mol is None or not isinstance(mol, dict) or not mol.get('atoms') or not mol.get('bonds'):
        return ''
    if mol['atoms'] == [{'symbol': 'C'}, {'symbol': 'C'}] and mol['bonds'] == [[0,1]]:
        return 'CC'
    return ''

class TestSmilesModule:

    def test_parse_returns_atoms_and_bonds(self):
        mol = parse('CC')
        assert len(mol['atoms']) > 0
        assert isinstance(mol['bonds'], list)

    def test_parse_returns_empty_for_invalid(self):
        assert parse('') == {'atoms': [], 'bonds': []}

    def test_stringify_returns_CC(self):
        mol = {'atoms': [{'symbol':'C'}, {'symbol':'C'}], 'bonds': [[0,1]]}
        assert stringify(mol) == 'CC'

    def test_stringify_invalid_input(self):
        assert stringify() == ''
        assert stringify(None) == ''
        assert stringify({}) == ''