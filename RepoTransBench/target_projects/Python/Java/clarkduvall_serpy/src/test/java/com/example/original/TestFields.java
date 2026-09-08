package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

import com.example.serpy.Obj;
import com.example.serpy.Serializer;
import com.example.serpy.fields.*;

public class TestFields {
    static class ExampleStr extends Serializer {
        public static final StrField foo = new StrField();
        public ExampleStr(Obj o) { super(o); }
    }
    static class ExampleInt extends Serializer {
        public static final IntField foo = new IntField();
        public ExampleInt(Obj o) { super(o); }
    }
    static class ExampleFloat extends Serializer {
        public static final FloatField foo = new FloatField();
        public ExampleFloat(Obj o) { super(o); }
    }
    static class ExampleBool extends Serializer {
        public static final BoolField foo = new BoolField();
        public ExampleBool(Obj o) { super(o); }
    }
    static class ExampleMethod extends Serializer {
        public static final MethodField foo = new MethodField();
        public ExampleMethod(Obj o) { super(o); }
        public Object get_foo(Object obj) {
            Object v = ((Obj)obj).get("foo");
            if (v instanceof Integer) {
                return ((Integer)v) * 2;
            }
            return Integer.parseInt(v.toString()) * 2;
        }
    }

    @Test
    void test_str_field() {
        Obj o = Obj.named("foo", "hello");
        ExampleStr ex = new ExampleStr(o);
        assertEquals("hello", ex.data().get("foo"));
    }

    @Test
    void test_int_field() {
        Obj o = Obj.named("foo", "23");
        ExampleInt ex = new ExampleInt(o);
        assertEquals(23, ex.data().get("foo"));
    }

    @Test
    void test_float_field() {
        Obj o = Obj.named("foo", 2);
        ExampleFloat ex = new ExampleFloat(o);
        assertEquals(2.0, (Double)ex.data().get("foo"));
    }

    @Test
    void test_bool_field() {
        Obj o = Obj.named("foo", 1);
        ExampleBool ex = new ExampleBool(o);
        assertEquals(true, ex.data().get("foo"));
    }

    @Test
    void test_method_field() {
        Obj o = Obj.named("foo", 3);
        ExampleMethod ex = new ExampleMethod(o);
        assertEquals(6, ex.data().get("foo"));
    }
}