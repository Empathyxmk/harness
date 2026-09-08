package com.hannesdorfmann.fragmentargs.processor;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Public test with different data for protected access logic.
 * The logic is the same as ProtectedAccessTest.
 */
public class ProtectedAccessPublicTest {

    @Test
    public void protectedFieldAccessTest_publicVariant() {
        DummyProtectedObjectPublic dummy = new DummyProtectedObjectPublic();
        // Use different data: original might use "foo", now use "barBaz"
        dummy.setValue("barBaz");
        assertEquals("barBaz", dummy.getValue());
    }

    // Static inner class mimicking the access logic for test
    static class DummyProtectedObjectPublic {
        protected String field;

        public void setValue(String val) {
            this.field = val;
        }

        public String getValue() {
            return this.field;
        }
    }
}