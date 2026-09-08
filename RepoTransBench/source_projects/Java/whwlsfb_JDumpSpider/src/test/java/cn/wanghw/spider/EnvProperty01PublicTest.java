package cn.wanghw.spider;

import org.junit.jupiter.api.*;
import cn.wanghw.*;

import java.util.*;

class EnvProperty01PublicTest {

    public class PublicDummyHeapHolder implements IHeapHolder {
        public Object findClass(String var1) { return (var1.equals("java.lang.PublicProcessEnvironment")) ? this : null; }
        public Iterator getClasses() { return null; }
        public boolean isInstanceOf(Object javaClass, String className) { return false; }
        public boolean isArray(Object javaClass) { return false; }
        public Object[] getSubClasses(Object javaClass) { return new Object[0]; }
        public List getInstances(Object javaClass) {
            List<Object> l = new ArrayList<>();
            l.add(new Object());
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
            m.put("PUBLIC_ENV", "VALUE42");
            return m;
        }
        public Object[] getArrayItems(Object instance) { return new Object[0]; }
        public String getFieldStringValue(Object instance, String fieldName) { return null; }
        public Object getFieldValue(Object instance, String fieldName) { return null; }
        public boolean isMap(Object instance) { return instance instanceof Map; }
        public Object getMap(Object instance) { return new HashMap<>(); }
        public String toString(Object instance) { return null; }
        public byte[] toByteArray(Object _instance) { return new byte[0]; }
    }

    @Test
    public void testGetNamePublic() {
        EnvProperty01 env = new EnvProperty01();
        Assertions.assertEquals("ProcessEnvironment", env.getName());
    }

    @Test
    public void testSniffHappyPathPublic() {
        EnvProperty01 env = new EnvProperty01();
        PublicDummyHeapHolder heapHolder = new PublicDummyHeapHolder();
        String s = env.sniff(heapHolder);
        Assertions.assertTrue(s.contains("PUBLIC_ENV"));
        Assertions.assertTrue(s.contains("VALUE42"));
    }

    @Test
    public void testSniffHandlesExceptionPublic() {
        EnvProperty01 env = new EnvProperty01();
        IHeapHolder heapHolder = new PublicDummyHeapHolder() {
            @Override
            public Object getMap(Object instance) { throw new RuntimeException("bad_public"); }
        };
        env.sniff(heapHolder); // should not throw!
    }

    @Test
    public void testSniffNoClassFoundPublic() {
        EnvProperty01 env = new EnvProperty01();
        IHeapHolder heapHolder = new PublicDummyHeapHolder() {
            @Override
            public Object findClass(String var1) { return null; }
        };
        Assertions.assertNull(env.sniff(heapHolder));
    }
}