package com.maxcountryman.flasklogin.original;

import com.maxcountryman.flasklogin.about.About;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestAbout {

    @Test
    public void testAboutWarns() {
        // Simulate deprecated warning via flag
        assertTrue(About.warned);
        assertEquals("Flask-Login", About.__title__);
        assertEquals("0.7.0", About.__version__);
    }

    @Test
    public void testVersionWarns() {
        // In Java, version lookup warnings cannot be replicated, simulate by reading About
        assertEquals(About.__version__, "0.7.0");
        // Simulate deprecation warning again
        assertTrue(About.warned);
    }

    @Test
    public void testVersionAttributeError() {
        // In Java, AttributeError maps to NoSuchFieldException/NoSuchMethodException
        try {
            java.lang.reflect.Field f = About.class.getDeclaredField("notarealattr");
            f.get(null);
            fail("Should throw NoSuchFieldException");
        } catch (NoSuchFieldException e) {
            assertEquals("notarealattr", e.getMessage());
        } catch (Exception e) {
            fail("Wrong exception: " + e);
        }
    }
}