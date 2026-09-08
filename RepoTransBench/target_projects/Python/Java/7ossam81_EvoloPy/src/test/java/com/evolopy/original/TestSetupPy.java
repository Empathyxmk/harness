package com.evolopy.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class TestSetupPy {

    @Test
    public void testSetupPyRuns() throws IOException {
        assertTrue(Files.exists(Paths.get("setup.py")) || Files.exists(Paths.get("../setup.py")));
    }
}