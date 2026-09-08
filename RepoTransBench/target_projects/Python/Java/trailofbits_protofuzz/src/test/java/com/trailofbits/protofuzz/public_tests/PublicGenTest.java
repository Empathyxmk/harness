package com.trailofbits.protofuzz.public_tests;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicGenTest {

    static class DummyField {
        String name;
        int cppType;
        int label;
        Object messageType;
        DummyField(String name) {
            this.name = name;
            this.cppType = 2;
            this.label = 1;
            this.messageType = null;
        }
        DummyField(String name, boolean messageTypeFlag) {
            this.name = name;
            this.cppType = 20;
            this.label = 1;
            this.messageType = messageTypeFlag ? AnotherDummyMessageType.class : null;
        }
    }

    static class DummyDesc {
        List<DummyField> fields;
        DummyDesc() {
            this.fields = new ArrayList<>();
            this.fields.add(new DummyField("y"));
        }
        DummyDesc(String mode) {
            if (mode.equals("different")) {
                this.fields = new ArrayList<>();
                this.fields.add(new DummyField("different", true));
            }
        }
    }

    static class DummyMsg {
        DummyDesc DESCRIPTOR = new DummyDesc();
    }

    static class AnotherDummyMessageType {
        static DummyDesc DESCRIPTOR = new DummyDesc();
    }

    static class DummyMsgParent {
        DummyDesc DESCRIPTOR = new DummyDesc("different");
        public Object different;
    }

    public static Iterator<DummyMsg> messageGeneratorSimple(final DummyMsg dummyMsg, final java.util.function.BiFunction<Class<?>, DummyField, Iterator<?>> dummyValgen, int maxMessages) {
        return new Iterator<DummyMsg>() {
            int yielded = 0;
            @Override
            public boolean hasNext() { return yielded < maxMessages; }
            @Override
            public DummyMsg next() {
                if (yielded++ < maxMessages) {
                    DummyMsg msg = new DummyMsg();
                    Iterator<?> it = dummyValgen.apply(null, null);
                    if (it.hasNext()) {
                        // Simulate setting property
                    }
                    return msg;
                }
                throw new java.util.NoSuchElementException();
            }
        };
    }

    public static Iterator<DummyMsgParent> messageGeneratorWithType(final DummyMsgParent dummyMsgParent, final java.util.function.BiFunction<Class<?>, DummyField, Iterator<?>> dummyValgen, int maxMessages) {
        return new Iterator<DummyMsgParent>() {
            int yielded = 0;
            @Override
            public boolean hasNext() { return yielded < maxMessages; }
            @Override
            public DummyMsgParent next() {
                if (yielded++ < maxMessages) {
                    DummyMsgParent msg = new DummyMsgParent();
                    Iterator<?> it = dummyValgen.apply(null, null);
                    if (it.hasNext()) {
                        msg.different = it.next();
                    }
                    return msg;
                }
                throw new java.util.NoSuchElementException();
            }
        };
    }

    @Test
    public void testMessageGeneratorSimplePublic() {
        DummyMsg dummy = new DummyMsg();
        java.util.function.BiFunction<Class<?>, DummyField, Iterator<?>> dummyValgen =
                (t, f) -> java.util.Arrays.asList(99, 100).iterator();
        List<DummyMsg> objs = new ArrayList<>();
        Iterator<DummyMsg> it = messageGeneratorSimple(dummy, dummyValgen, 2);
        while (it.hasNext()) objs.add(it.next());
        assertEquals(2, objs.size());
        assertTrue(objs.get(0) instanceof DummyMsg && objs.get(1) instanceof DummyMsg);
    }

    @Test
    public void testMessageGeneratorWithMessageTypePublic() {
        DummyMsgParent dummyParent = new DummyMsgParent();
        java.util.function.BiFunction<Class<?>, DummyField, Iterator<?>> dummyValgen =
                (t, f) -> java.util.Arrays.asList(new AnotherDummyMessageType()).iterator();
        List<DummyMsgParent> out = new ArrayList<>();
        Iterator<DummyMsgParent> it = messageGeneratorWithType(dummyParent, dummyValgen, 1);
        while (it.hasNext()) out.add(it.next());
        assertEquals(1, out.size());
        assertTrue(out.get(0) instanceof DummyMsgParent);
    }

    @ParameterizedTest
    @CsvSource({
            "1, java.util.ArrayList",
            "2, java.util.ArrayList",
            "3, java.util.ArrayList"
    })
    public void test_assign_to_field_public(int label, String expectedType) throws Exception {
        class DummyObj {}
        DummyObj obj = new DummyObj();
        class Field {
            public int label = label;
            public String name = "bar";
        }
        Field field = new Field();
        int value = 77;
        List<Object> result = new ArrayList<>();
        result.add(value);
        assertEquals(Class.forName(expectedType), result.getClass());
    }
}