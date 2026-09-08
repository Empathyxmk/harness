package io.paperdb;

import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import static androidx.test.InstrumentationRegistry.getTargetContext;
import static junit.framework.Assert.assertEquals;
import static junit.framework.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

@RunWith(AndroidJUnit4.class)
public class CustomBookPublicTest {

    @Before
    public void setUp() {
        Paper.init(getTargetContext());
    }

    @Test
    public void getFolderPathForBook_custom_public() {
        String path = Paper.book("public_custom").getPath();
        assertTrue(path.endsWith("/io.paperdb.test/files/public_custom"));
    }

    @Test
    public void getFilePathForKey_customBook_public() {
        String path = Paper.book("public_custom").getPath("my_val");
        assertTrue(path.endsWith("/io.paperdb.test/files/public_custom/my_val.pt"));
    }

    @Test
    public void readWriteDeleteToDifferentBooks_public() {
        String publicBook = "public_custom";
        Paper.book().destroy();
        Paper.book(publicBook).destroy();

        Paper.book().write("country", "Denmark");
        Paper.book(publicBook).write("country", "Norway");

        assertEquals("Denmark", Paper.book().read("country"));
        assertEquals("Norway", Paper.book(publicBook).read("country"));

        Paper.book().delete("country");
        assertFalse(Paper.book().contains("country"));
        assertTrue(Paper.book(publicBook).contains("country"));
    }
}