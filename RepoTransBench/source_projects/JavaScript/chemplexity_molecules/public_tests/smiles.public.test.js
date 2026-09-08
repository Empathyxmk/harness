import { parse, stringify } from '../src/main/smiles.js';

describe('SMILES module (public)', () => {
    test('parse returns atoms and bonds for a different string', () => {
        const mol = parse('CO');
        expect(mol.atoms.length).toBeGreaterThan(0);
        expect(Array.isArray(mol.bonds)).toBe(true);
    });

    test('parse returns empty for whitespace', () => {
        expect(parse('   ')).toEqual({ atoms: [], bonds: [] });
    });

    test('stringify returns "CO" for molecule', () => {
        // Dummy molecule object as parse stub
        const mol = { atoms: [{symbol: 'C'}, {symbol: 'O'}], bonds: [[0,1]] };
        expect(stringify(mol)).toBe('CO');
    });

    test('stringify returns empty for array input', () => {
        expect(stringify([])).toBe('');
    });
    test('stringify returns empty for false input', () => {
        expect(stringify(false)).toBe('');
    });
});