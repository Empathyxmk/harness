package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestPublicDumpToolExtra {

    @Test
    public void test_public_dumpxls_patch() throws Exception {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        output.write(new byte[]{(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1});
        byte[] val = output.toByteArray();
        assertArrayEquals(new byte[]{(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1},
                          Arrays.copyOf(val, 8));
    }
}