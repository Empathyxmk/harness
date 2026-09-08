package cn.wanghw.spider;

import org.junit.jupiter.api.*;
import cn.wanghw.*;

import java.util.*;

class DataSource04PublicTest {

    class PublicDummyHeapHolder implements IHeapHolder {
        public Object findClass(String var1) { return (var1.contains("AnotherDruidDataSourceWrapper")) ? this : null; }
        public Iterator getClasses() { return null; }
        public boolean isInstanceOf(Object javaClass, String className) { return true; }
        public boolean isArray(Object javaClass) { return true; }
        public Object[] getSubClasses(Object javaClass) { return new Object[]{"pubsub"}; }
        public List getInstances(Object javaClass) {
            List<Object> l = new ArrayList<>();
            l.add(new Object());
            l.add(new Object());
            return l;
        }
        public List getFields(Object javaClass) { return Collections.singletonList("pubfield"); }
        public String getClassName(Object javaClass) { return "pubClazz"; }
        public Object getSuperClass(Object javaClass) { return null; }
        public String getFieldName(Object field) { return ""; }
        public Object getFieldClass(Object field) { return ""; }
        public Object findThing(Long objectId) { return null; }
        public Object getValueOfField(Object instance, String fieldName) { return null; }
        public HashMap<String, String> getFieldsByNameList(Object instance, HashMap<String, String> fieldList) {
            HashMap<String, String> ret = new HashMap<>();
            ret.put("username", "pubuser");
            ret.put("password", "pubpass");
            ret.put("jdbcUrl", "jdbc:oracle://newhost/db");
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
    public void testGetNamePublic() {
        DataSource04 ds = new DataSource04();
        Assertions.assertEquals("AliDruidDataSourceWrapper", ds.getName());
    }

    @Test
    public void testSniffNoClassFoundPublic() {
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
    public void testSniffHappyPathPublic() {
        DataSource04 ds = new DataSource04();
        PublicDummyHeapHolder heapHolder = new PublicDummyHeapHolder();
        String result = ds.sniff(heapHolder);
        Assertions.assertTrue(result.contains("pubuser"));
        Assertions.assertTrue(result.contains("pubpass"));
        Assertions.assertTrue(result.contains("jdbc:oracle://newhost/db"));
    }

    @Test
    public void testSniffHandlesExceptionPublic() {
        DataSource04 ds = new DataSource04();
        IHeapHolder heapHolder = new PublicDummyHeapHolder() {
            @Override
            public List getInstances(Object javaClass) {
                throw new RuntimeException("publicFail");
            }
        };
        ds.sniff(heapHolder); // should not throw!
    }
}