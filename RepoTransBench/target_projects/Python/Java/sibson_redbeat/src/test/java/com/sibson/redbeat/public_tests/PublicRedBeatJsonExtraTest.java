package com.sibson.redbeat.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class PublicRedBeatJsonExtraTest {

    @Test
    public void testPassthroughEntryPublic() {
        String orig = "{\"publickey\": \"publicval\"}";
        String result = RedBeatStubHelpers.passthroughJson(orig);
        assertEquals(orig, result);
    }
}