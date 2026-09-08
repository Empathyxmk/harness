import * as math from '../src/utilities/math.js';

describe('math.matrix (public)', () => {
    it('zeros creates different zero matrix', () => {
        const res = math.zeros(3, 1);
        expect(res).toEqual([[0],[0],[0]]);
    });

    it('ones creates different ones matrix', () => {
        const res = math.ones(1, 3);
        expect(res).toEqual([[1,1,1]]);
    });

    it('can add two different matrices', () => {
        const a = [[2,4,6],[8,10,12]];
        const b = [[1,3,5],[7,9,11]];
        expect(math.add(a, b)).toEqual([[3,7,11],[15,19,23]]);
    });

    it('can subtract two different matrices', () => {
        const a = [[9,8],[7,6]];
        const b = [[5,4],[3,2]];
        expect(math.subtract(a, b)).toEqual([[4,4],[4,4]]);
    });

    it('can multiply two different matrices', () => {
        const a = [[2,0],[1,3]];
        const b = [[1,4],[0,2]];
        expect(math.multiply(a, b)).toEqual([[2,8],[1,10]]);
    });

    it('can multiply matrix by another scalar', () => {
        const a = [[2,4],[6,8]];
        expect(math.multiply(a, 2)).toEqual([[4,8],[12,16]]);
    });

    it('identity matrix with different square values', () => {
        const a = [[9,8],[7,6]];
        expect(math.identity(a)).toEqual([[1,0],[0,1]]);
    });

    it('inverse returns null for another non-square matrix', () => {
        const A = [[1,2],[3,4],[5,6]];
        expect(math.inverse(A)).toEqual(null);
    });

    // Additional edge case, different sizes
    it('zeros works with single column', () => {
        expect(math.zeros(4, 1)).toEqual([[0],[0],[0],[0]]);
    });
    it('ones works with single row', () => {
        expect(math.ones(1, 5)).toEqual([[1,1,1,1,1]]);
    });

    it('multiply throws on another invalid sizes', () => {
        expect(() => math.multiply([[1,2,3]], [[1,2]])).toThrow('Matrix size mismatch');
    });

    // Inverse for another invertible 2x2
    it('inverse for different invertible 2x2', () => {
        const A = [[3,8],[4,6]];
        const inv = math.inverse(A);
        expect(inv[0][0]).toBeCloseTo(-0.6);
        expect(inv[0][1]).toBeCloseTo(0.8);
        expect(inv[1][0]).toBeCloseTo(0.4);
        expect(inv[1][1]).toBeCloseTo(-0.3);
    });

    // Another singular 2x2
    it('inverse for another singular 2x2 is null', () => {
        const A = [[1,2],[2,4]];
        expect(math.inverse(A)).toEqual(null);
    });

    it('identity on different empty matrix returns empty', () => {
        expect(math.identity([[]])).toEqual([[]]);
    });

    // Invalid inverse input with array of wrong shape and with object
    it('inverse with array shape MxN (non-square) returns null', () => {
        expect(math.inverse([[1,2,3]])).toEqual(null);
    });
    it('inverse with object input returns null', () => {
        expect(math.inverse({a:1, b:2})).toEqual(null);
    });
});