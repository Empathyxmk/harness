package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.example.serpy.Obj;
import com.example.serpy.Serializer;
import com.example.serpy.fields.*;

import java.util.*;

public class PublicTestFields {

    @Test
    void test_str_field() {
        class TestSerializer extends Serializer {
            public static final StrField foo = new StrField();
            public TestSerializer(Obj o) { super(o); }
        }
        Obj o = Obj.named("foo", "differentstr");
        TestSerializer ser = new TestSerializer(o);
        assertEquals(Map.of("foo", "differentstr"), ser.data());
    }

    @Test
    void test_int_field() {
        class TestSerializer extends Serializer {
            public static final IntField bar = new IntField();
            public TestSerializer(Obj o) { super(o); }
        }
        Obj o = Obj.named("bar", 100);
        TestSerializer ser = new TestSerializer(o);
        assertEquals(Map.of("bar", 100), ser.data());
    }

    @Test
    void test_method_field() {
        class TestSerializer extends Serializer {
            public static final MethodField special = new MethodField();
            public TestSerializer(Obj o) { super(o); }
            public Object get_special(Object obj) {
                Object v = ((Obj)obj).get("foo");
                return v != null ? v.toString().toUpperCase() : null;
            }
        }
        Obj o = Obj.named("foo", "public");
        TestSerializer ser = new TestSerializer(o);
        assertEquals(Map.of("special", "PUBLIC"), ser.data());
    }

    @Test
    void test_missing_value_field() {
        class TestSerializer extends Serializer {
            public static final MethodField bar = new MethodField();
            public TestSerializer(Obj o) { super(o); }
            public Object get_bar(Object obj) {
                return ((Obj)obj).has("bar") ? ((Obj)obj).get("bar") : null;
            }
        }
        Obj o = new Obj();
        TestSerializer ser = new TestSerializer(o);
        assertEquals(Map.of("bar", null), ser.data());
    }
}