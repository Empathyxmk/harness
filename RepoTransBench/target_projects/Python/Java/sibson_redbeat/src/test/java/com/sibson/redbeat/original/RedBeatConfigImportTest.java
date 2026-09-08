package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatConfigImportTest {
    @Test
    public void testConfigStubImport() {
        assertNotNull(new RedBeatConfigStub(new AppStub()));
    }
}