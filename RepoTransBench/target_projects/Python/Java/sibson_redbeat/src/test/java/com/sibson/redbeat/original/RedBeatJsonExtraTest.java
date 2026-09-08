package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatJsonExtraTest {

    @Test
    public void testPassthroughEntry() {
        String orig = "{\"key\": \"val\"}";
        String result = RedBeatStubHelpers.passthroughJson(orig);
        assertEquals(orig, result);
    }

    @Test
    public void testPassthroughNotType() {
        assertEquals("somevalue", RedBeatStubHelpers.passthroughJson("somevalue"));
    }
}