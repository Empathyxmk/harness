package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class CharacterCompositeTest {

    @Test
    void testAddAndCount() {
        CharacterComposite composite = new CharacterComposite() {};
        assertEquals(0, composite.count());
        composite.add(new CharacterComposite() {});
        assertEquals(1, composite.count());
    }

    @Test
    void testPrintNoChildren() {
        CharacterComposite composite = new CharacterComposite() {};
        // Just verify it does not throw
        composite.print();
    }

    @Test
    void testPrintBeforeAfterHooks() {
        class TestComposite extends CharacterComposite {
            boolean beforeCalled = false;
            boolean afterCalled = false;
            @Override
            public void printBefore() { beforeCalled = true; }
            @Override
            public void printAfter() { afterCalled = true; }
        }
        TestComposite composite = new TestComposite();
        composite.print();
        assertTrue(composite.beforeCalled);
        assertTrue(composite.afterCalled);
    }

    @Test
    void testPrintDeepComposition() {
        StringBuilder sb = new StringBuilder();
        CharacterComposite composite = new CharacterComposite() {
            @Override
            public void printBefore() { sb.append("["); }
            @Override
            public void printAfter() { sb.append("]"); }
        };

        CharacterComposite child = new CharacterComposite() {
            @Override
            public void printBefore() { sb.append("A"); }
        };
        composite.add(child);
        composite.print();
        assertEquals("[A]", sb.toString());
    }
}