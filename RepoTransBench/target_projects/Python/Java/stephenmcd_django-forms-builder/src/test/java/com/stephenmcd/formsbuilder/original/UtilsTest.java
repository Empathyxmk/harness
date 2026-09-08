package com.stephenmcd.formsbuilder.original;

import com.stephenmcd.formsbuilder.utils.Utils;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class UtilsTest {

    @Test
    public void testIsFileExtensions() {
        assertTrue(Utils.isFile("photo.PNG"));
        assertTrue(Utils.isFile("document.PDF"));
        assertFalse(Utils.isFile("example.txt"));
        assertFalse(Utils.isFile("no_dot"));
    }

    @Test
    public void testSlugifyBasic() {
        String s = " Hello__World__ ";
        String sl = Utils.slugify(s);
        assertEquals("hello-world", sl);
    }

    @Test
    public void testIsEmailCases() {
        assertTrue(Utils.isEmail("foo@bar.com"));
        assertFalse(Utils.isEmail("notanemail"));
        assertFalse(Utils.isEmail("@nodomain"));
    }

    @Test
    public void testContentAsTxtHtml() {
        class Dummy {
            @Override
            public String toString() {
                return "dummyContent";
            }
        }
        String text = Utils.contentAsText(new Dummy());
        String html = Utils.contentAsHtml(new Dummy());
        assertTrue(text instanceof String);
        assertTrue(html instanceof String);
    }

    @Test
    public void testGetAdminUrlFormat() {
        class Dummy {
            // Simulate needed attributes
        }
        String url = Utils.getAdminUrl(new Dummy());
        assertTrue(url.contains("myapp/dummy/1/") || url.contains("myapp/dummy/1"));
    }
}