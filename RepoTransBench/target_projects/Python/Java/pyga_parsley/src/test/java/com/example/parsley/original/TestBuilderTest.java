package com.example.parsley.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestBuilderTest {

    @Test
    public void testBuilderAddsAtoms() {
        Builder b = new Builder();
        b.addAtom("foo");
        b.addAtom("bar");
        assertEquals(2, b.size());
        assertEquals("foo", b.get(0));
        assertEquals("bar", b.get(1));
    }

    @Test
    public void testBuilderClear() {
        Builder b = new Builder();
        b.addAtom("baz");
        b.clear();
        assertEquals(0, b.size());
    }
}

class Builder {
    private final java.util.List<String> atoms = new java.util.ArrayList<>();
    void addAtom(String a) { atoms.add(a); }
    int size() { return atoms.size(); }
    String get(int i) { return atoms.get(i); }
    void clear() { atoms.clear(); }
}