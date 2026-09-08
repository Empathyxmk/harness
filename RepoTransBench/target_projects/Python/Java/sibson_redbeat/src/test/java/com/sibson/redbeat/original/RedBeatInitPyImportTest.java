package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatInitPyImportTest {
    @Test
    public void testImportsPresent() {
        assertNotNull(RedBeatSchedulerStub.class);
        assertNotNull(RedBeatSchedulerEntryStub.class);
    }
}