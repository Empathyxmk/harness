package org.caoym.jjvm.lang;

import org.junit.Test;
import static org.junit.Assert.*;

public class JvmFieldMethodPublicTest {

    @Test
    public void testAccessDifferentPrimitiveFields() {
        JvmField intField = new JvmField("score", "I", 7, false);
        JvmField boolField = new JvmField("visible", "Z", true, false);

        assertEquals(7, intField.getValue());
        assertEquals(true, boolField.getValue());

        intField.setValue(42);
        assertEquals(42, intField.getValue());

        boolField.setValue(false);
        assertEquals(false, boolField.getValue());
    }

    @Test
    public void testStringFieldDifferentValue() {
        JvmField strField = new JvmField("owner", "Ljava/lang/String;", "robot", false);
        assertEquals("robot", strField.getValue());

        strField.setValue("android");
        assertEquals("android", strField.getValue());
    }
}