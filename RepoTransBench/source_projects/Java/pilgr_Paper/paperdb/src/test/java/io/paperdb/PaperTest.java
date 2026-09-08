package io.paperdb;

import android.content.Context;

import org.junit.Test;

import java.io.File;

import static org.junit.Assert.*;

public class PaperTest {

    static class DummyContext extends android.test.mock.MockContext {
        @Override
        public File getFilesDir() {
            return new File(System.getProperty("java.io.tmpdir"));
        }

        @Override
        public Context getApplicationContext() {
            return this;
        }
    }

    @Test
    public void testInitAndBookDefault() {
        Paper.init(new DummyContext());
        Book book = Paper.book();
        assertNotNull(book);
    }

    @Test
    public void testBookWithName() {
        Paper.init(new DummyContext());
        Book book = Paper.book("myBook");
        assertNotNull(book);
    }

    @Test
    public void testBookOnLocation() {
        Paper.init(new DummyContext());
        String path = System.getProperty("java.io.tmpdir");
        Book book = Paper.bookOn(path, "namedbook");
        assertNotNull(book);
    }

    @Test
    public void testRemoveLastSeparator() {
        String sep = File.separator;
        String result = PaperTestInvokeRemoveLastFS("path" + sep);
        assertEquals("path", result);
        result = PaperTestInvokeRemoveLastFS("path");
        assertEquals("path", result);
    }

    @Test(expected = PaperDbException.class)
    public void testGetBookThrowsWithoutInit() {
        // Not calling Paper.init
        Paper.book();
    }

    @Test(expected = PaperDbException.class)
    public void testBookNameThrowsDefaultName() {
        Paper.init(new DummyContext());
        Paper.book("io.paperdb");
    }

    // Helper to access private static from Paper
    public static String PaperTestInvokeRemoveLastFS(String s) {
        try {
            java.lang.reflect.Method m = Paper.class.getDeclaredMethod("removeLastFileSeparatorIfExists", String.class);
            m.setAccessible(true);
            return (String) m.invoke(null, s);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}