package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.XContentTypeOptions;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestXContentTypeOptions {

    @Test
    public void testDefaultXContentTypeOptions() {
        XContentTypeOptions x = new XContentTypeOptions();
        assertEquals("nosniff", x.getHeaderValue());
    }

    @Test
    public void testSetCustomValue() {
        XContentTypeOptions x = new XContentTypeOptions().set("custom-value");
        assertEquals("custom-value", x.getHeaderValue());
    }

    @Test
    public void testNosniff() {
        XContentTypeOptions x = new XContentTypeOptions().nosniff();
        assertEquals("nosniff", x.getHeaderValue());
    }

    @Test
    public void testClear() {
        XContentTypeOptions x = new XContentTypeOptions().set("custom-value").clear();
        assertEquals("nosniff", x.getHeaderValue());
    }
}