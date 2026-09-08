package net.jodah.typetools;

import org.junit.jupiter.api.Test;
import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;

class TypeDescriptorTest {
    @Test
    void testPrimitiveTypesAreSingletons() {
        assertNotNull(TypeDescriptor.BOOLEAN_TYPE);
        assertNotNull(TypeDescriptor.BYTE_TYPE);
        assertNotNull(TypeDescriptor.CHAR_TYPE);
        assertNotNull(TypeDescriptor.DOUBLE_TYPE);
        assertNotNull(TypeDescriptor.FLOAT_TYPE);
        assertNotNull(TypeDescriptor.INT_TYPE);
    }
}