package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class TestPublicLoad {

    @Test
    void testPublicLoadBuffer() throws IOException {
        String arff = "@RELATION abcd\n@DATA\n10";
        BufferedReader reader = new BufferedReader(new StringReader(arff));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line).append("\n");
        assertTrue(sb.toString().contains("@RELATION"));
        assertTrue(sb.toString().contains("@DATA"));
    }
}