package me.zbl.composite;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CharacterCompositePublicTest {

    @Test
    void testAddMultipleAndCountPublic() {
        CharacterComposite composite = new CharacterComposite() {};
        assertEquals(0, composite.count());
        composite.add(new CharacterComposite() {});
        composite.add(new CharacterComposite() {});
        assertEquals(2, composite.count());
    }

    @Test
    void testPrintNoChildrenPublic() {
        CharacterComposite composite = new CharacterComposite() {};
        // Just verify it does not throw for empty
        composite.print();
    }

    @Test
    void testPrintBeforeAfterHooksPublic() {
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
    void testPrintDeepCompositionPublic() {
        StringBuilder sb = new StringBuilder();
        CharacterComposite composite = new CharacterComposite() {
            @Override
            public void printBefore() { sb.append("<"); }
            @Override
            public void printAfter() { sb.append(">"); }
        };

        CharacterComposite child = new CharacterComposite() {
            @Override
            public void printBefore() { sb.append("B"); }
        };
        composite.add(child);
        composite.print();
        assertEquals("<B>", sb.toString());
    }
}