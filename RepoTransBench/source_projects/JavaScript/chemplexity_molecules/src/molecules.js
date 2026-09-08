// Patch import to use .js file extension for Node ESM loader compatibility
// and allow successful test/coverage runs for downstream code that imports this module
import { parse, stringify } from './main/smiles.js';

export function getMoleculeFromSMILES(smiles) {
    return parse(smiles);
}

export function getSMILESFromMolecule(molecule) {
    return stringify(molecule);
}