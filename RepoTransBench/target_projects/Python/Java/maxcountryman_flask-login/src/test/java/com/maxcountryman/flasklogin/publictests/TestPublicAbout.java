package com.maxcountryman.flasklogin.publictests;

import com.maxcountryman.flasklogin.about.About;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicAbout {

    @Test
    public void testAboutWarnsPublic() {
        assertTrue(About.warned);
        assertTrue(About.__title__.contains("Flask"));
        assertTrue(About.__version__.split("\\.").length == 3);
    }

    @Test
    public void testInitDunderVersionWarnsPublic() {
        assertEquals(About.__version__, "0.7.0");
        assertTrue(About.warned);
    }

    @Test
    public void testInitDunderVersionAttributeErrorPublic() {
        try {
            java.lang.reflect.Field f = About.class.getDeclaredField("certainlynotanattribute");
            f.get(null);
            fail("Should throw NoSuchFieldException");
        } catch (NoSuchFieldException e) {
            assertEquals("certainlynotanattribute", e.getMessage());
        } catch (Exception e) {
            fail("Wrong exception: " + e);
        }
    }
}