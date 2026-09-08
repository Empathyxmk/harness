package cn.wanghw.spider;

import org.junit.jupiter.api.*;
import cn.wanghw.*;

import java.util.*;

class EnvProperty01Test {

    public class DummyHeapHolder implements IHeapHolder {
        public Object findClass(String var1) { return (var1.equals("java.lang.ProcessEnvironment")) ? this : null; }
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
        public String getClassName(Object javaClass) { return null; }
        public Object getSuperClass(Object javaClass) { return null; }
        public String getFieldName(Object field) { return null; }
        public Object getFieldClass(Object field) { return null; }
        public Object findThing(Long objectId) { return null; }
        public Object getValueOfField(Object instance, String fieldName) { return null; }
        public HashMap<String, String> getFieldsByNameList(Object instance, HashMap<String, String> fieldList) { return new HashMap<>(); }
        public HashMap<String, String> arrayDump(Object instance) {
            HashMap<String, String> m = new HashMap<>();
            m.put("ENVVAR", "VAL");
            return m;
        }
        public Object[] getArrayItems(Object instance) { return new Object[0]; }
        public String getFieldStringValue(Object instance, String fieldName) { return null; }
        public Object getFieldValue(Object instance, String fieldName) { return null; }
        public boolean isMap(Object instance) { return instance instanceof Map; }
        public Object getMap(Object instance) { return new Object(); }
        public String toString(Object instance) { return null; }
        public byte[] toByteArray(Object _instance) { return new byte[0]; }
    }

    @Test
    public void testGetName() {
        EnvProperty01 env = new EnvProperty01();
        Assertions.assertEquals("ProcessEnvironment", env.getName());
    }

    @Test
    public void testSniffHappyPath() {
        EnvProperty01 env = new EnvProperty01();
        DummyHeapHolder heapHolder = new DummyHeapHolder();
        String s = env.sniff(heapHolder);
        Assertions.assertTrue(s.contains("ENVVAR"));
        Assertions.assertTrue(s.contains("VAL"));
    }

    @Test
    public void testSniffHandlesException() {
        EnvProperty01 env = new EnvProperty01();
        IHeapHolder heapHolder = new DummyHeapHolder() {
            @Override
            public Object getMap(Object instance) { throw new RuntimeException("bad"); }
        };
        env.sniff(heapHolder); // should not throw!
    }

    @Test
    public void testSniffNoClassFound() {
        EnvProperty01 env = new EnvProperty01();
        IHeapHolder heapHolder = new DummyHeapHolder() {
            @Override
            public Object findClass(String var1) { return null; }
        };
        Assertions.assertNull(env.sniff(heapHolder));
    }
}