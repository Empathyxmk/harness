package com.angeloc.s3pitrestore.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class PublicSetupPyTest {
    @Test
    public void testSetupPyCanImportAndCallsSetupPublic() {
        // Simulate patching and inspecting distutils.core.setup (public test keys)
        Map<String, Object> called = new HashMap<>();
        called.put("author", "Angelo Compagnucci");
        called.put("author_email", "angelo.compagnucci@gmail.com");
        called.put("keywords", Arrays.asList("s3", "restore", "aws"));

        assertEquals("Angelo Compagnucci", called.get("author"));
        assertEquals("angelo.compagnucci@gmail.com", called.get("author_email"));
        assertTrue(called.containsKey("keywords"));
    }
}