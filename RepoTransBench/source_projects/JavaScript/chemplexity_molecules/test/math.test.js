import * as math from '../src/utilities/math.js';

describe('math.matrix', () => {
    it('zeros creates zero matrix', () => {
        const res = math.zeros(2, 3);
        expect(res).toEqual([[0,0,0],[0,0,0]]);
    });

    it('ones creates ones matrix', () => {
        const res = math.ones(2, 2);
        expect(res).toEqual([[1,1],[1,1]]);
    });

    it('can add two matrices', () => {
        const a = [[1,2],[3,4]];
        const b = [[4,3],[2,1]];
        expect(math.add(a, b)).toEqual([[5,5],[5,5]]);
    });

    it('can subtract two matrices', () => {
        const a = [[5,7],[1,9]];
        const b = [[2,3],[1,2]];
        expect(math.subtract(a, b)).toEqual([[3,4],[0,7]]);
    });

    it('can multiply two matrices', () => {
        const a = [[1,2],[3,4]];
        const b = [[2,0],[1,2]];
        expect(math.multiply(a, b)).toEqual([[4,4],[10,8]]);
    });

    it('can multiply matrix by a scalar', () => {
        const a = [[1,2],[3,4]];
        expect(math.multiply(a, 3)).toEqual([[3,6],[9,12]]);
    });

    it('identity matrix returns ones on diagonal', () => {
        const a = [[5,6],[7,8]];
        expect(math.identity(a)).toEqual([[1,0],[0,1]]);
    });

    it('inverse returns null for non-square matrix', () => {
        const A = [[1,2,3],[4,5,6]];
        expect(math.inverse(A)).toEqual(null);
    });

    // Additional edge case: test zeros and ones 1D input
    it('zeros works with single rows', () => {
        expect(math.zeros(1, 4)).toEqual([[0,0,0,0]]);
    });
    it('ones works with single columns', () => {
        expect(math.ones(3, 1)).toEqual([[1],[1],[1]]);
    });

    // Coverage for edge, test that multiply throws on bad shapes
    it('multiply throws on invalid sizes', () => {
        expect(() => math.multiply([[1,2]], [[1,2]])).toThrow('Matrix size mismatch');
    });

    // Coverage for 2x2 inverse logic
    it('inverse for invertible 2x2', () => {
        const A = [[4,7],[2,6]];
        const inv = math.inverse(A);
        expect(inv[0][0]).toBeCloseTo(0.6);
        expect(inv[0][1]).toBeCloseTo(-0.7);
        expect(inv[1][0]).toBeCloseTo(-0.2);
        expect(inv[1][1]).toBeCloseTo(0.4);
    });

    // 2x2 singular
    it('inverse for singular 2x2 is null', () => {
        const A = [[2,4],[1,2]];
        expect(math.inverse(A)).toEqual(null);
    });

    // Coverage for identity for empty array
    it('identity on empty matrix returns empty', () => {
        expect(math.identity([])).toEqual([]);
    });

    // Invalid inverse input
    it('inverse with invalid input returns null', () => {
        expect(math.inverse("bad")).toEqual(null);
    });
});