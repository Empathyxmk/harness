package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.scripts.ReadZBar;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestReadZbarPublic {

    @Test
    void testGetArgsQrcode() {
        ReadZBar.Args args = ReadZBar.getArgs(new String[]{"barcode_testimage.png"});
        assertEquals("barcode_testimage.png", args.file);
        // Use a less common flag -v (simulate verbose)
        ReadZBar.Args args2 = ReadZBar.getArgs(new String[]{"-v", "--"});
        assertTrue(args2.verbose);
    }

    @Test
    void testMainNoFile() {
        assertThrows(IllegalArgumentException.class, () -> ReadZBar.getArgs(new String[]{}));
    }
}