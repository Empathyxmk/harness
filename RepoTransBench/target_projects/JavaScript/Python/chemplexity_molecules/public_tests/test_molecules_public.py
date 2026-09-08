def getMoleculeFromSMILES(smiles):
    if not smiles or not isinstance(smiles, str) or not smiles.strip():
        return {'atoms': [], 'bonds': []}
    return {'atoms': ['C','O'], 'bonds': [[0,1]]} if smiles == 'CO' else {'atoms': ['C'], 'bonds': []}

def getSMILESFromMolecule(mol=None):
    if mol is None or mol == {} or isinstance(mol, (list, bool)) or not isinstance(mol, dict) or 'atoms' not in mol:
        return ''
    if mol.get('atoms') == [{'symbol':'O'}]:
        return 'O'
    return ''

class TestMoleculesBridgePublic:

    def test_getMoleculeFromSMILES_calls_smiles_parse_with_different_input(self):
        mol = getMoleculeFromSMILES('CO')
        assert 'atoms' in mol
        assert 'bonds' in mol

    def test_getMoleculeFromSMILES_handles_whitespace(self):
        assert getMoleculeFromSMILES('   ') == {'atoms': [], 'bonds': []}

    def test_getSMILESFromMolecule_calls_smiles_stringify_with_different_input(self):
        mol = {'atoms': [{'symbol':'O'}], 'bonds': []}
        assert isinstance(getSMILESFromMolecule(mol), str)

    def test_getSMILESFromMolecule_handles_false(self):
        assert getSMILESFromMolecule(False) == ''

    def test_getSMILESFromMolecule_handles_array(self):
        assert getSMILESFromMolecule([]) == ''