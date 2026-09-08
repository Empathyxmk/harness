package com.evolopy.public_tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;

public class TestSetupPyPublic {

    @Test
    public void testReadmeExistsAndNotEmptyPublic() throws IOException {
        assertTrue(Files.exists(Paths.get("README.md")));
        String content = Files.readString(Paths.get("README.md"));
        assertTrue(content.trim().length() > 10);
    }
}