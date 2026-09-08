package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

class RedirectTest {
    @Test
    void testWriteToFileAndRead() throws Exception {
        File file = File.createTempFile("redirect_test_", ".txt");
        file.deleteOnExit();

        String msg = "Hello, Redirect!";
        try (PrintWriter out = new PrintWriter(new FileWriter(file))) {
            out.print(msg);
        }

        StringBuilder inMsg = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = in.readLine()) != null) {
                inMsg.append(line);
            }
        }
        assertEquals(msg, inMsg.toString());
    }
}