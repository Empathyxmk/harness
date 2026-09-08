package net.jodah.typetools;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TypeDescriptorPublicTest {
    @Test
    void testOtherPrimitiveTypesAreSingletons() {
        assertNotNull(TypeDescriptor.LONG_TYPE);
        assertNotNull(TypeDescriptor.SHORT_TYPE);
    }
}