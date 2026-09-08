package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class TestLoad {

    @Test
    void testLoadStream() throws IOException {
        String arff = "@RELATION info\n@DATA\n5";
        BufferedReader reader = new BufferedReader(new StringReader(arff));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line).append("\n");
        assertTrue(sb.toString().contains("@RELATION"));
        assertTrue(sb.toString().contains("@DATA"));
    }
}