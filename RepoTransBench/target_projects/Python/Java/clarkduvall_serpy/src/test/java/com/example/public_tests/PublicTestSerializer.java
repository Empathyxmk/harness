package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.example.serpy.Obj;
import com.example.serpy.Serializer;
import com.example.serpy.fields.*;

import java.util.*;

class AnotherPublicSerializer extends Serializer {
    public static final StrField name = new StrField();
    public static final IntField value = new IntField();
    public AnotherPublicSerializer(Obj o) { super(o); }
    public AnotherPublicSerializer(List<Obj> os) { super(os, true); }
}

class MethodPublicSerializer extends Serializer {
    public static final StrField foo = new StrField();
    public static final MethodField doubleField = new MethodField("double");
    public MethodPublicSerializer(Obj o) { super(o); }
    public MethodPublicSerializer(List<Obj> os) { super(os, true); }
    public Object get_double(Object obj) {
        Object v = ((Obj)obj).get("foo");
        return v != null ? v.toString() + v.toString() : null;
    }
}

public class PublicTestSerializer {

    @Test
    void test_serializer_basic() {
        Obj o = Obj.named("name","other","value",13);
        AnotherPublicSerializer ser = new AnotherPublicSerializer(o);
        assertEquals(Map.of("name", "other", "value", 13), ser.data());
    }

    @Test
    void test_serializer_many() {
        List<Obj> objects = Arrays.asList(
                Obj.named("name","x","value",2),
                Obj.named("name","y","value",7)
        );
        AnotherPublicSerializer ser = new AnotherPublicSerializer(objects);
        List<Map<String,Object>> expected = Arrays.asList(
                Map.of("name", "x", "value", 2),
                Map.of("name", "y", "value", 7)
        );
        assertEquals(expected, ser.getData());
    }

    @Test
    void test_method_serializer() {
        Obj o = Obj.named("foo","hello");
        MethodPublicSerializer ser = new MethodPublicSerializer(o);
        assertEquals(Map.of("foo", "hello", "double", "hellohello"), ser.data());
    }

    @Test
    void test_method_serializer_many() {
        List<Obj> objects = Arrays.asList(
                Obj.named("foo","abc"),
                Obj.named("foo","de")
        );
        MethodPublicSerializer ser = new MethodPublicSerializer(objects);
        List<Map<String,Object>> expected = Arrays.asList(
                Map.of("foo", "abc", "double", "abcabc"),
                Map.of("foo", "de", "double", "dede")
        );
        assertEquals(expected, ser.getData());
    }
}