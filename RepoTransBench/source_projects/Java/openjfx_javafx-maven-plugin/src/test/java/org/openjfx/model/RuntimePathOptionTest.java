package org.openjfx.model;

import org.junit.Test;
import static org.junit.Assert.*;

public class RuntimePathOptionTest {

    @Test
    public void testEnumValues() {
        assertEquals(RuntimePathOption.CLASSPATH, RuntimePathOption.valueOf("CLASSPATH"));
        assertEquals(RuntimePathOption.MODULEPATH, RuntimePathOption.valueOf("MODULEPATH"));
        assertEquals(2, RuntimePathOption.values().length);
    }
}