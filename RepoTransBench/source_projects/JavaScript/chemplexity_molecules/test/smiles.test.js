import { parse, stringify } from '../src/main/smiles.js';

describe('SMILES module', () => {
    test('parse returns atoms and bonds for string', () => {
        const mol = parse('CC');
        expect(mol.atoms.length).toBeGreaterThan(0);
        expect(Array.isArray(mol.bonds)).toBe(true);
    });

    test('parse returns empty for invalid', () => {
        expect(parse('')).toEqual({ atoms: [], bonds: [] });
    });

    test('stringify returns "CC" for molecule', () => {
        // Construct dummy molecule object as in parse stub
        const mol = { atoms: [{symbol: 'C'}, {symbol: 'C'}], bonds: [[0,1]] };
        expect(stringify(mol)).toBe('CC');
    });

    test('stringify returns empty for invalid input', () => {
        expect(stringify()).toBe('');
        expect(stringify(null)).toBe('');
        expect(stringify({})).toBe('');
    });
});