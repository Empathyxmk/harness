import * as molecules from '../src/molecules.js';

describe('molecules bridge', () => {
    it('getMoleculeFromSMILES calls smiles.parse', () => {
        const mol = molecules.getMoleculeFromSMILES('CC');
        expect(mol).toHaveProperty('atoms');
        expect(mol).toHaveProperty('bonds');
    });

    it('getMoleculeFromSMILES handles empty string', () => {
        expect(molecules.getMoleculeFromSMILES('')).toEqual({ atoms: [], bonds: [] });
    });

    it('getSMILESFromMolecule calls smiles.stringify', () => {
        const mol = { atoms: [{symbol:'C'}], bonds: [] };
        expect(typeof molecules.getSMILESFromMolecule(mol)).toBe('string');
    });

    it('getSMILESFromMolecule handles undefined', () => {
        expect(molecules.getSMILESFromMolecule()).toBe('');
    });

    it('getSMILESFromMolecule handles empty object', () => {
        expect(molecules.getSMILESFromMolecule({})).toBe('');
    });
});