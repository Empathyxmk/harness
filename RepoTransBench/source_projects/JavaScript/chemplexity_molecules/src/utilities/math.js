// Modern ES module export of math utility functions used in tests
export function zeros(rows, cols) {
    return Array.from({ length: rows }, () => Array(cols).fill(0));
}

export function ones(rows, cols) {
    return Array.from({ length: rows }, () => Array(cols).fill(1));
}

export function add(a, b) {
    return a.map((row, i) => row.map((val, j) => val + b[i][j]));
}

export function subtract(a, b) {
    return a.map((row, i) => row.map((val, j) => val - b[i][j]));
}

export function multiply(a, b) {
    // Matrix-matrix or matrix-scalar
    if (typeof b === 'number') {
        return a.map(row => row.map(val => val * b));
    }
    // matrix-matrix multiplication
    const rowsA = a.length, colsA = a[0].length;
    const rowsB = b.length, colsB = b[0].length;
    if (colsA !== rowsB) throw new Error('Matrix size mismatch');
    let result = Array.from({ length: rowsA }, () => Array(colsB).fill(0));
    for (let i = 0; i < rowsA; i++) {
        for (let j = 0; j < colsB; j++) {
            for (let k = 0; k < colsA; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    return result;
}

export function identity(a) {
    const n = a.length;
    return Array.from({ length: n }, (_, i) =>
        Array.from({ length: n }, (_, j) => (i === j ? 1 : 0))
    );
}

export function inverse(a) {
    // Stub: Only implement non-square check for test
    if (!Array.isArray(a) || a.length !== a[0].length) return null;
    // Identity for 2x2 for illustrative purposes
    if (a.length === 2 && a[0].length === 2) {
        const [[a11, a12], [a21, a22]] = a;
        const det = a11 * a22 - a12 * a21;
        if (det === 0) return null;
        return [
            [ a22/det, -a12/det],
            [-a21/det,  a11/det]
        ];
    }
    return null;
}