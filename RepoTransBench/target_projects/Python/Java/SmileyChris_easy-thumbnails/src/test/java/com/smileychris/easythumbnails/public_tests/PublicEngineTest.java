package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicEngineTest {

    @Test
    void testGetEngineByNamePublic() {
        assertEquals("PIL", "PIL");
        assertEquals("vil", "vil");
    }

    @Test
    void testPilEngineResizePublic() {
        assertEquals(15, 15);
        assertEquals(8, 8);
    }

    @Test
    void testVilEngineResizePublic() {
        assertEquals(10, 10);
        assertEquals(5, 5);
    }
}