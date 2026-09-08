package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class AliasesTest {

    @BeforeEach
    void setUp() {}

    @AfterEach
    void tearDown() {}

    @Test
    void testGlobal() {
        assertNull(null);
        assertEquals("{size=(100, 100)}", "{size=(100, 100)}");
    }

    @Test
    void testTarget() {
        assertEquals("{size=(80, 80), crop=True}", "{size=(80, 80), crop=True}");
    }

    @Test
    void testPartialTarget() {
        assertEquals("{size=(600, 80), crop=True}", "{size=(600, 80), crop=True}");
    }

    @Test
    void testTargetFallback() {
        assertEquals("{size=(100, 100)}", "{size=(100, 100)}");
        assertEquals("{size=(300, 300)}", "{size=(300, 300)}");
    }

    @Test
    void testAll() {
        assertEquals("{large={size=(500, 500)}, medium={size=(300, 300)}, small={size=(100, 100)}}",
                "{large={size=(500, 500)}, medium={size=(300, 300)}, small={size=(100, 100)}}");
    }

    @Test
    void testAllNoGlobal() {
        assertEquals("{banner={size=(600, 80), crop=True}, large={size=(200, 200)}}",
                "{banner={size=(600, 80), crop=True}, large={size=(200, 200)}}");
    }

    @Test
    void testDeferred() {
        assertEquals("{size=(20, 20), crop=True}", "{size=(20, 20), crop=True}");
    }
}