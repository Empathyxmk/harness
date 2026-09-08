package cn.wanghw;

import org.junit.jupiter.api.*;
import java.io.*;
import java.util.*;
import java.lang.reflect.Field;

class PublicDummyHeapHolder implements IHeapHolder {
    // Slightly different return values to exercise code
    public Object findClass(String var1) { return "publicDummyClass"; }
    public Iterator getClasses() { return Collections.emptyIterator(); }
    public boolean isInstanceOf(Object javaClass, String className) { return true; }
    public boolean isArray(Object javaClass) { return true; }
    public Object[] getSubClasses(Object javaClass) { return new Object[]{"sub1"}; }
    public List getInstances(Object javaClass) { return Collections.singletonList("instance"); }
    public List getFields(Object javaClass) { return Collections.singletonList("field"); }
    public String getClassName(Object javaClass) { return "publicDummyClass"; }
    public Object getSuperClass(Object javaClass) { return "publicSuperClass"; }
    public String getFieldName(Object field) { return "fieldName"; }
    public Object getFieldClass(Object field) { return "fieldClass"; }
    public Object findThing(Long objectId) { return "foundThing"; }
    public Object getValueOfField(Object instance, String fieldName) { return "valueOfField"; }
    public HashMap<String, String> getFieldsByNameList(Object instance, HashMap<String, String> fieldList) {
        HashMap<String, String> m = new HashMap<>();
        m.put("username", "publicU");
        m.put("password", "publicP");
        m.put("jdbcUrl", "jdbc:public");
        return m;
    }
    public HashMap<String, String> arrayDump(Object instance) { return new HashMap<>(); }
    public Object[] getArrayItems(Object instance) { return new Object[]{"item1", "item2"}; }
    public String getFieldStringValue(Object instance, String fieldName) { return "stringValue"; }
    public Object getFieldValue(Object instance, String fieldName) { return "fieldValue"; }
    public boolean isMap(Object instance) { return true; }
    public Object getMap(Object instance) { return new HashMap<String, String>(); }
    public String toString(Object instance) { return "toStringResult"; }
    public byte[] toByteArray(Object _instance) { return new byte[]{1,2,3}; }
}

class PublicDummySpider implements ISpider {
    public String getName() { return "publicDummy"; }
    public String sniff(IHeapHolder heapHolder) { return "public_sniffed"; }
}

public class MainPublicTest {

    @Test
    public void testRunWithHelpFlagShowsHelpMessage() throws Exception {
        String out = Main.run(new String[]{"-help"});
        // Add a case that prints help
        Assertions.assertTrue(out.contains("usage"));
    }

    @Test
    public void testRunWithNonexistentFileShowsMessageDifferentName() throws Exception {
        String[] args = { "totally_missing_file.hprof" };
        String out = Main.run(args);
        Assertions.assertTrue(out.toLowerCase().contains("file not exist"));
    }

    @Test
    public void testRunAsyncRequiresResultPathDifferentHeap() throws Exception {
        String result = Main.runAsync(new String[] {"randomheap.hprof"});
        Assertions.assertTrue(result.toLowerCase().contains("must give a result file path"));
    }

    @Test
    public void testGetArgValueThrowsOnDifferentFlag() throws Exception {
        Main m = new Main();
        // -in is present, but no value after it
        Field f = Main.class.getDeclaredField("flag");
        f.setAccessible(true);
        List<String> flist = new LinkedList<>();
        flist.add("-in");
        f.set(m, flist);
        Exception ex = Assertions.assertThrows(Exception.class, () -> {
            m.getClass().getDeclaredMethod("getArgValue", String.class).setAccessible(true);
            m.getClass().getDeclaredMethod("getArgValue", String.class).invoke(m, "-in");
        });
        Assertions.assertTrue(ex.getMessage().toLowerCase().contains("get '-in' value failed"));
    }

    @Test
    public void testGetFileVersionBadFileDifferent() throws Exception {
        Main m = new Main();
        // Set up a different phantom file name
        Field field = Main.class.getDeclaredField("heapfile");
        field.setAccessible(true);
        field.set(m, new File("definitely_nonexistent_file.file"));
        Assertions.assertThrows(RuntimeException.class, () -> m.getFileVersion());
    }
}