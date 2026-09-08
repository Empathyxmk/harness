package org.caoym.jjvm.lang;

import org.caoym.jjvm.runtime.Env;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class JvmFieldMethodTest {
    @Test
    void testJvmField() throws Exception {
        JvmField field = new JvmField() {
            private Object v;
            @Override
            public void set(Env env, Object thiz, Object value) {
                v = value;
            }

            @Override
            public Object get(Env env, Object thiz) {
                return v;
            }
        };
        field.set(null, null, "abc");
        assertEquals("abc", field.get(null, null));
    }

    @Test
    void testJvmMethod() throws Exception {
        JvmMethod method = new JvmMethod() {
            boolean called = false;
            @Override public void call(Env env, Object thiz, Object... args) { called = true; }
            @Override public int getParameterCount() { return 1; }
            @Override public String getName() { return "hello"; }
        };
        method.call(null, null, new Object[]{});
        assertEquals(1, method.getParameterCount());
        assertEquals("hello", method.getName());
    }
}