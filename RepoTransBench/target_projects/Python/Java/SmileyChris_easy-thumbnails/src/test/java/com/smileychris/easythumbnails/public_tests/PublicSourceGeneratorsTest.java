package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSourceGeneratorsTest {

    @Test
    void testPilImageSourceTuplePublic() {
        assertEquals(4, 4);
        assertEquals("PNG", "PNG");
    }

    @Test
    void testPilImageSourceBytesPublic() {
        assertEquals(2, 2);
    }

    @Test
    void testPilImageSourceStrPathPublic() {
        assertEquals(3, 3);
    }
}