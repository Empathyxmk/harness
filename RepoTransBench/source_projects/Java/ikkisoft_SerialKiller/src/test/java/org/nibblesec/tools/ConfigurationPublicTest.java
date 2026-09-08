package org.nibblesec.tools;

import org.junit.Test;

import java.util.Properties;

import static org.junit.Assert.*;

public class ConfigurationPublicTest {
    @Test
    public void testPropertyLoadDifferentKey() {
        Properties props = new Properties();
        props.setProperty("public.test.key", "publicValue");
        assertNotNull(props.getProperty("public.test.key"));
        assertEquals("publicValue", props.getProperty("public.test.key"));
        assertNull(props.getProperty("nonexistent.key"));
    }
}