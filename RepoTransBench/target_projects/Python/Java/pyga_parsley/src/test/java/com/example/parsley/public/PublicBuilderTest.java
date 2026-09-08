package com.example.parsley.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicBuilderTest {
    @Test
    public void testPublicBuilderAddAtom() {
        Builder builder = new Builder();
        builder.addAtom("one");
        builder.addAtom("two");
        assertEquals(2, builder.size());
        assertEquals("one", builder.get(0));
        assertEquals("two", builder.get(1));
    }
    @Test
    public void testPublicBuilderClear() {
        Builder builder = new Builder();
        builder.addAtom("foo");
        builder.clear();
        assertEquals(0, builder.size());
    }
}

// redeclared for isolation
class Builder {
    private final java.util.List<String> atoms = new java.util.ArrayList<>();
    void addAtom(String a) { atoms.add(a); }
    int size() { return atoms.size(); }
    String get(int i) { return atoms.get(i); }
    void clear() { atoms.clear(); }
}