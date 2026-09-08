import * as molecules from '../src/molecules.js';

describe('molecules bridge (public)', () => {
    it('getMoleculeFromSMILES calls smiles.parse with different input', () => {
        const mol = molecules.getMoleculeFromSMILES('CO');
        expect(mol).toHaveProperty('atoms');
        expect(mol).toHaveProperty('bonds');
    });

    it('getMoleculeFromSMILES handles whitespace', () => {
        expect(molecules.getMoleculeFromSMILES('   ')).toEqual({ atoms: [], bonds: [] });
    });

    it('getSMILESFromMolecule calls smiles.stringify with different input', () => {
        const mol = { atoms: [{symbol:'O'}], bonds: [] };
        expect(typeof molecules.getSMILESFromMolecule(mol)).toBe('string');
    });

    it('getSMILESFromMolecule handles false', () => {
        expect(molecules.getSMILESFromMolecule(false)).toBe('');
    });

    it('getSMILESFromMolecule handles array', () => {
        expect(molecules.getSMILESFromMolecule([])).toBe('');
    });
});