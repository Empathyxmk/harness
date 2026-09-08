package cn.wanghw.spider;

import org.junit.jupiter.api.*;
import cn.wanghw.*;

import java.util.*;

class DataSource04Test {

    class DummyHeapHolder implements IHeapHolder {
        public Object findClass(String var1) { return (var1.contains("DruidDataSourceWrapper")) ? this : null; }
        public Iterator getClasses() { return null; }
        public boolean isInstanceOf(Object javaClass, String className) { return false; }
        public boolean isArray(Object javaClass) { return false; }
        public Object[] getSubClasses(Object javaClass) { return new Object[0]; }
        public List getInstances(Object javaClass) { 
            List<Object> l = new ArrayList<>(); 
            l.add(new Object()); 
            return l; 
        }
        public List getFields(Object javaClass) { return new ArrayList(); }
        public String getClassName(Object javaClass) { return "clazz"; }
        public Object getSuperClass(Object javaClass) { return null; }
        public String getFieldName(Object field) { return ""; }
        public Object getFieldClass(Object field) { return ""; }
        public Object findThing(Long objectId) { return null; }
        public Object getValueOfField(Object instance, String fieldName) { return null; }
        public HashMap<String, String> getFieldsByNameList(Object instance, HashMap<String, String> fieldList) {
            HashMap<String, String> ret = new HashMap<>();
            ret.put("username", "user");
            ret.put("password", "pass");
            ret.put("jdbcUrl", "jdbc:mysql://localhost/x");
            return ret;
        }
        public HashMap<String, String> arrayDump(Object instance) { return new HashMap<>(); }
        public Object[] getArrayItems(Object instance) { return new Object[0]; }
        public String getFieldStringValue(Object instance, String fieldName) { return ""; }
        public Object getFieldValue(Object instance, String fieldName) { return null; }
        public boolean isMap(Object instance) { return false; }
        public Object getMap(Object instance) { return null; }
        public String toString(Object instance) { return ""; }
        public byte[] toByteArray(Object _instance) { return new byte[0]; }
    }

    @Test
    public void testGetName() {
        DataSource04 ds = new DataSource04();
        Assertions.assertEquals("AliDruidDataSourceWrapper", ds.getName());
    }

    @Test
    public void testSniffNoClassFound() {
        DataSource04 ds = new DataSource04();
        IHeapHolder dummy = new IHeapHolder() {
            public Object findClass(String var1) { return null; }
            public Iterator getClasses() { return null; }
            public boolean isInstanceOf(Object javaClass, String className) { return false; }
            public boolean isArray(Object javaClass) { return false; }
            public Object[] getSubClasses(Object javaClass) { return new Object[0]; }
            public List getInstances(Object javaClass) { return new ArrayList(); }
            public List getFields(Object javaClass) { return new ArrayList(); }
            public String getClassName(Object javaClass) { return null; }
            public Object getSuperClass(Object javaClass) { return null; }
            public String getFieldName(Object field) { return null; }
            public Object getFieldClass(Object field) { return null; }
            public Object findThing(Long objectId) { return null; }
            public Object getValueOfField(Object instance, String fieldName) { return null; }
            public HashMap<String, String> getFieldsByNameList(Object instance, HashMap<String, String> fieldList) { return new HashMap<>(); }
            public HashMap<String, String> arrayDump(Object instance) { return new HashMap<>(); }
            public Object[] getArrayItems(Object instance) { return new Object[0]; }
            public String getFieldStringValue(Object instance, String fieldName) { return null; }
            public Object getFieldValue(Object instance, String fieldName) { return null; }
            public boolean isMap(Object instance) { return false; }
            public Object getMap(Object instance) { return null; }
            public String toString(Object instance) { return null; }
            public byte[] toByteArray(Object _instance) { return new byte[0]; }
        };
        Assertions.assertNull(ds.sniff(dummy));
    }

    @Test
    public void testSniffHappyPath() {
        DataSource04 ds = new DataSource04();
        DummyHeapHolder heapHolder = new DummyHeapHolder();
        String result = ds.sniff(heapHolder);
        Assertions.assertTrue(result.contains("user"));
        Assertions.assertTrue(result.contains("pass"));
        Assertions.assertTrue(result.contains("jdbc:mysql://localhost/x"));
    }

    @Test
    public void testSniffHandlesException() {
        DataSource04 ds = new DataSource04();
        IHeapHolder heapHolder = new DummyHeapHolder() {
            @Override
            public List getInstances(Object javaClass) {
                throw new RuntimeException("fail");
            }
        };
        // Should log and not throw, should not throw to test!
        ds.sniff(heapHolder);
    }
}