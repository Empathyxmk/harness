package com.backblaze.erasure;

import org.junit.Test;
import static org.junit.Assert.*;

public class MatrixPublicTest {
    @Test
    public void testMatrixMultiplicationDifferentValues() {
        byte[][] a = new byte[][] {
            {11, 22},
            {33, 44}
        };
        byte[][] b = new byte[][] {
            {2, 1},
            {0, 3}
        };
        byte[][] expected = new byte[][] {
            {(byte)(11*2+22*0), (byte)(11*1+22*3)},
            {(byte)(33*2+44*0), (byte)(33*1+44*3)}
        };

        byte[][] actual = multiply(a, b);
        assertArrayEquals(expected[0], actual[0]);
        assertArrayEquals(expected[1], actual[1]);
    }

    private byte[][] multiply(byte[][] a, byte[][] b) {
        int n = a.length, m = b[0].length, p = b.length;
        byte[][] c = new byte[n][m];
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                for (int k = 0; k < p; ++k)
                    c[i][j] += a[i][k] * b[k][j];
        return c;
    }
}