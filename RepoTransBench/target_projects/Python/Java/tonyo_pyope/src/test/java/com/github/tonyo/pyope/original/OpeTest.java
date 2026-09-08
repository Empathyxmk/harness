package com.github.tonyo.pyope.original;

import com.github.tonyo.pyope.ope.OPE;
import com.github.tonyo.pyope.ope.ValueRange;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class OpeTest {

    @Test
    void testOrderGuarantees() {
        // Test that encryption is order-preserving
        int[] values = {0, 1, 2, 10, 28, 42, 1000, 1001, (int)Math.pow(2, 15) - 1};
        byte[] key = "key".getBytes();
        OPE cipher = new OPE(key);
        List<Long> encryptedValues = new ArrayList<>();
        for (int value : values) {
            encryptedValues.add(cipher.encrypt(value));
        }
        List<Long> sorted = new ArrayList<>(new HashSet<>(encryptedValues));
        Collections.sort(sorted);
        assertEquals(encryptedValues, sorted, "Order is not preserved");
    }

    @Test
    void testOpeEncryptDecrypt() {
        // Encrypt and then decrypt
        long[] values = {-1000, -100, -20, -1, 0, 1, 10, 100, 314, 1337, 1338, 10000};
        byte[] key = "key".getBytes();
        ValueRange inRange = new ValueRange(-1000, (long)Math.pow(2, 20));
        ValueRange outRange = new ValueRange(-10000, (long)Math.pow(2, 32));
        OPE cipher = new OPE(key, inRange, outRange);
        List<Long> encryptedValues = new ArrayList<>();
        for (long value : values) {
            encryptedValues.add(cipher.encrypt(value));
        }
        OPE cipherDec = new OPE(key, inRange, outRange);
        for (int i = 0; i < values.length; i++) {
            long decrypted = cipherDec.decrypt(encryptedValues.get(i));
            assertEquals(values[i], decrypted, "Dec(Enc(P)) != P");
        }
    }

    @Test
    void testOpeDeterministic() {
        // Test that encrypting the same values yields the same results
        int[] values = {0, 314, 1337, 1338, 10000};
        OPE cipher = new OPE("key-la-la".getBytes());
        List<Long> encryptedFirst = new ArrayList<>();
        for (int value : values) {
            encryptedFirst.add(cipher.encrypt(value));
        }
        List<Long> encryptedSecond = new ArrayList<>();
        for (int value : values) {
            encryptedSecond.add(cipher.encrypt(value));
        }
        assertEquals(encryptedFirst, encryptedSecond);
    }

    @Test
    void testDenseRange() {
        // Equal ranges must yield 1-to-1 mapping
        int rangeStart = 0;
        int rangeEnd = (int)Math.pow(2, 15);
        ValueRange inRange = new ValueRange(rangeStart, rangeEnd);
        ValueRange outRange = inRange.copy();
        byte[] key = "123".getBytes();
        OPE cipher = new OPE(key, inRange, outRange);
        int[] values = {0, 10, 20, 50, 100, 1000, (int)Math.pow(2, 10), (int)Math.pow(2, 15)};
        for (int v : values) {
            assertEquals(v, cipher.encrypt(v));
            assertEquals(v, cipher.decrypt(v));
        }
        assertThrows(Exception.class, () -> {
            new OPE(key, new ValueRange(0, 10), new ValueRange(1, 2));
        });
    }

    @Test
    void testLongDifferentKeys() {
        // Test that different keys yield different ciphertexts
        byte[] key1 = new byte[]{0x12,0x23,0x34,0x45,0x56,0x67,0x78,(byte)0x89,(byte)0x90,0x0A,(byte)0xAB,(byte)0xBC,(byte)0xCD,(byte)0xDE,(byte)0xEF,(byte)0xF0,0x13,0x14,0x15,0x16};
        byte[] key2 = new byte[]{0x0A,(byte)0xAB,(byte)0xBC,(byte)0xCD,(byte)0xDE,(byte)0xEF,(byte)0xF0,0x13,0x14,0x15,0x16,0x12,0x23,0x34,0x45,0x56,0x67,0x78,(byte)0x89,(byte)0x90,0x12,0x13};
        OPE ope1 = new OPE(key1);
        OPE ope2 = new OPE(key2);
        int[] values = {0, 1, 10, 100, 1000, 2000, 3000, 4000, 5000};
        for (int v : values) {
            assertNotEquals(ope1.encrypt(v), ope2.encrypt(v));
        }
    }

    @Test
    void testEncryptSmallOutRangeIssue() {
        // Regression test for https://github.com/tonyo/pyope/issues/13
        OPE cipher = new OPE("fresh key".getBytes(),
                new ValueRange(0, 2), new ValueRange(2, 5));
        assertNotNull(cipher.encrypt(0));
        assertNotNull(cipher.encrypt(1));
        assertNotNull(cipher.encrypt(2));
    }

    @Test
    void testBigRanges() {
        ValueRange inRange = new ValueRange((long)Math.pow(2, 32), (long)Math.pow(2, 33));
        ValueRange outRange = new ValueRange((long)Math.pow(2, 48), (long)Math.pow(2, 49));
        OPE ope = new OPE("test-big-ranges".getBytes(), inRange, outRange);
        long plaintext = inRange.getStart();
        while (plaintext <= inRange.getEnd()) {
            assertNotNull(ope.encrypt(plaintext));
            plaintext += (long)Math.pow(2, 24);
        }
    }

    @Test
    void testHugeOutputRange() {
        // Regression test for https://github.com/tonyo/pyope/pull/16
        OPE cipher = new OPE("key11".getBytes(),
                new ValueRange(0, 0), new ValueRange(0, (long)Math.pow(2, 65)));
        assertNotNull(cipher.encrypt(0));
    }
}