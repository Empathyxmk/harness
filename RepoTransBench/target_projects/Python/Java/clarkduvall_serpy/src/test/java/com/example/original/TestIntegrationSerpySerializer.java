package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

import com.example.serpy.Obj;
import com.example.serpy.Serializer;
import com.example.serpy.DictSerializer;
import com.example.serpy.fields.*;

class DummyObj {
    public int a;
    public int b;
    public int method_val;
    public Object c;

    public DummyObj() {
        this(1, 2, null, 5);
    }
    public DummyObj(int a, int b) {
        this(a, b, null, 5);
    }
    public DummyObj(int a, int b, Object c, int method_val) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.method_val = method_val;
    }
    public int meth() { return method_val; }
}

public class TestIntegrationSerpySerializer {

    static class Ex extends Serializer {
        public static final IntField a = new IntField();
        public static final IntField b = new IntField();
        public Ex(DummyObj o) { super(o); }
    }

    static class ExMethod extends Serializer {
        public static final MethodField foo = new MethodField("maybe");
        public ExMethod(DummyObj o) { super(o); }
        public Object get_foo(Object obj) { return ((DummyObj)obj).method_val; }
    }

    static class DSer extends DictSerializer {
        public static final IntField x = new IntField();
        public static final IntField y = new IntField();
        public DSer(Map<String, Integer> map) { super(map); }
    }

    static class ExampleWithRepr extends Serializer {
        public static final FieldImpl foo = new FieldImpl();
        public ExampleWithRepr(Obj o) { super(o); }
    }

    @Test
    void test_simple_serialization() {
        DummyObj o = new DummyObj(4, 5);
        Ex ex = new Ex(o);
        Map<String, Object> result = ex.data();
        assertEquals(Map.of("a", 4, "b", 5), result);
    }

    @Test
    void test_method_and_custom_labels() {
        DummyObj o = new DummyObj(1,2,null,42);
        ExMethod em = new ExMethod(o);
        Map<String,Object> data = em.data();
        assertTrue(data.containsKey("maybe"));
        assertEquals(42, data.get("maybe"));
    }

    @Test
    void test_dict_serializer() {
        Map<String,Integer> d = new HashMap<>();
        d.put("x", 10);
        d.put("y", 21);
        DSer ser = new DSer(d);
        Map<String,Object> result = ser.data();
        assertEquals(Map.of("x",10,"y",21), result);
    }

    @Test
    void test_edge_cases_and_repr() {
        Obj o = Obj.named("foo", "edgecase");
        ExampleWithRepr ex = new ExampleWithRepr(o);
        String repr = ex.toString();
        assertTrue(repr.contains("ExampleWithRepr"));
    }
}