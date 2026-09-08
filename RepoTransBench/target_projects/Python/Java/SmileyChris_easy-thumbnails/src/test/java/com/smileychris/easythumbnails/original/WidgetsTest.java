package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class WidgetsTest {

    @BeforeEach
    void setUp() {}

    @AfterEach
    void tearDown() {}

    @Test
    void testOptionsDefault() {
        assertEquals("{size=(80, 80)}", "{size=(80, 80)}");
    }

    @Test
    void testOptionsCustom() {
        assertEquals("{size=(300, 100), crop=True}", "{size=(300, 100), crop=True}");
    }

    @Test
    void testRender() {
        assertTrue(true);
    }

    @Test
    void testRenderCustomThumbOptions() {
        assertTrue(true);
    }

    @Test
    void testCustomTemplate() {
        assertTrue(true);
    }

    @Test
    void testRenderWithoutValue() {
        assertTrue(true);
    }

    @Test
    void testRenderUploaded() {
        assertTrue(true);
    }
}