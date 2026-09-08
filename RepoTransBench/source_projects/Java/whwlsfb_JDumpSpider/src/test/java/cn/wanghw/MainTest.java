package cn.wanghw;

import org.junit.jupiter.api.*;
import java.io.*;
import java.util.*;
import java.lang.reflect.Field;

class DummyHeapHolder implements IHeapHolder {
    // Methods return default/dummy values for test stub
    public Object findClass(String var1) { return "dummyClass"; }
    public Iterator getClasses() { return Collections.emptyIterator(); }
    public boolean isInstanceOf(Object javaClass, String className) { return false; }
    public boolean isArray(Object javaClass) { return false; }
    public Object[] getSubClasses(Object javaClass) { return new Object[0]; }
    public List getInstances(Object javaClass) { return new ArrayList(); }
    public List getFields(Object javaClass) { return new ArrayList(); }
    public String getClassName(Object javaClass) { return "dummyClass"; }
    public Object getSuperClass(Object javaClass) { return null; }
    public String getFieldName(Object field) { return ""; }
    public Object getFieldClass(Object field) { return ""; }
    public Object findThing(Long objectId) { return null; }
    public Object getValueOfField(Object instance, String fieldName) { return null; }
    public HashMap<String, String> getFieldsByNameList(Object instance, HashMap<String, String> fieldList) { 
        HashMap<String, String> m = new HashMap<>();
        m.put("username", "u");
        m.put("password", "p");
        m.put("jdbcUrl", "j");
        return m;
    }
    public HashMap<String, String> arrayDump(Object instance) { return new HashMap<>(); }
    public Object[] getArrayItems(Object instance) { return new Object[0]; }
    public String getFieldStringValue(Object instance, String fieldName) { return ""; }
    public Object getFieldValue(Object instance, String fieldName) { return null; }
    public boolean isMap(Object instance) { return false; }
    public Object getMap(Object instance) { return new HashMap<String, String>(); }
    public String toString(Object instance) { return ""; }
    public byte[] toByteArray(Object _instance) { return new byte[0]; }
}


class DummySpider implements ISpider {
    public String getName() { return "dummy"; }
    public String sniff(IHeapHolder heapHolder) { return "sniffed"; }
}

public class MainTest {

    @Test
    public void testRunWithNoArgsShowsMessage() throws Exception {
        String out = Main.run(new String[]{});
        Assertions.assertTrue(out.contains("please give a heap filepath"));
    }

    @Test
    public void testRunWithNonexistentFileShowsMessage() throws Exception {
        String[] args = { "nonexistent_file.hprof" };
        String out = Main.run(args);
        Assertions.assertTrue(out.contains("file not exist"));
    }

    @Test
    public void testRunAsyncRequiresResultPath() throws Exception {
        String result = Main.runAsync(new String[] {"heap.hprof"});
        Assertions.assertTrue(result.contains("must give a result file path"));
    }

    @Test
    public void testGetArgValueThrowsOnError() throws Exception {
        Main m = new Main();
        // -out is present, but no value after
        Field f = Main.class.getDeclaredField("flag");
        f.setAccessible(true);
        List<String> flist = new LinkedList<>();
        flist.add("-out");
        f.set(m, flist);
        Exception ex = Assertions.assertThrows(Exception.class, () -> {
            m.getClass().getDeclaredMethod("getArgValue", String.class).setAccessible(true);
            m.getClass().getDeclaredMethod("getArgValue", String.class).invoke(m, "-out");
        });
        Assertions.assertTrue(ex.getMessage().contains("Get '-out' value failed"));
    }

    @Test
    public void testGetFileVersionBadFile() throws Exception {
        Main m = new Main();
        // Set up a file that doesn't exist for heapfile to force exception
        Field field = Main.class.getDeclaredField("heapfile");
        field.setAccessible(true);
        field.set(m, new File("nope.file.that.is.never.there"));
        Assertions.assertThrows(RuntimeException.class, () -> m.getFileVersion());
    }
}