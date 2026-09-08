package com.backblaze.erasure;

import org.junit.Test;
import static org.junit.Assert.*;

public class GaloisPublicTest {
    @Test
    public void testGaloisMultiplyOtherData() {
        assertEquals(18, Galois.multiply((byte)6, (byte)3));
    }

    @Test
    public void testGaloisInverseOther() {
        byte input = 9;
        byte inv = Galois.inverse(input);
        assertEquals(57, inv & 0xFF); // known inverse in GF(2^8)
    }

    @Test
    public void testGaloisExpLogOtherData() {
        for (int i = 30; i < 35; i++) {
            int logVal = Galois.log((byte) i);
            int expVal = Galois.exp((byte) logVal);
            assertEquals(i, expVal);
        }
    }
}