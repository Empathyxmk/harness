package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

import com.example.serpy.Obj;
import com.example.serpy.Serializer;
import com.example.serpy.fields.*;

public class TestSerializer {
    static class ExampleLabel extends Serializer {
        public static final FieldImpl foo_label = new FieldImpl("foo", "foo_out");
        public ExampleLabel(Obj o) { super(o); }
    }
    static class ExampleInts extends Serializer {
        public static final IntField one = new IntField();
        public static final IntField two = new IntField();
        public ExampleInts(Obj o) { super(o); }
    }
    static class ExampleMissingAttr extends Serializer {
        public static final FieldImpl foo = new FieldImpl("bar");
        public ExampleMissingAttr(Obj o) { super(o); }
    }

    @Test
    void test_label_field() {
        Obj o = Obj.named("foo", "thing");
        ExampleLabel ex = new ExampleLabel(o);
        assertEquals("thing", ex.data().get("foo_out"));
    }

    @Test
    void test_serializer_to_value() {
        Obj o = Obj.named("one", 1, "two", 2);
        ExampleInts ex = new ExampleInts(o);
        assertEquals(Map.of("one",1,"two",2), ex.toValue(o));
    }

    @Test
    void test_missing_attr() {
        Obj o = Obj.named("bar", "baz");
        ExampleMissingAttr ex = new ExampleMissingAttr(o);
        assertEquals("baz", ex.data().get("foo"));
    }
}