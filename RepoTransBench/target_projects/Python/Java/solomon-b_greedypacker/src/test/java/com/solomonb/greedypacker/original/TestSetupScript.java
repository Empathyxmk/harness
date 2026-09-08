package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.Test;
import java.io.*;
import static org.junit.jupiter.api.Assertions.*;

class TestSetupScript {

    @Test
    void testSetupPyExists() {
        // Just check that setup.py exists, and that it mentions setuptools
        File f = new File("setup.py");
        assertTrue(f.exists(), "setup.py must exist in project root");
        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
            char[] buf = new char[200];
            int n = br.read(buf, 0, 200);
            String content = new String(buf, 0, n);
            assertTrue(content.contains("setuptools"), "setup.py must mention setuptools");
        } catch (IOException e) {
            fail("setup.py should be readable without error");
        }
    }
}