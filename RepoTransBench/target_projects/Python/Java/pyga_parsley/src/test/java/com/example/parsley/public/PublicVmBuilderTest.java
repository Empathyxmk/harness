package com.example.parsley.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicVmBuilderTest {
    @Test
    public void testVMBuilder() {
        VmBuilder builder = new VmBuilder();
        builder.add("X");
        builder.add("Y");
        assertEquals(2, builder.instructionsCount());
        assertEquals("X", builder.get(0));
        assertEquals("Y", builder.get(1));
    }
}

// redeclared for isolation
class VmBuilder {
    private final java.util.List<String> instructions = new java.util.ArrayList<>();
    public void add(String i) { instructions.add(i); }
    public int instructionsCount() { return instructions.size(); }
    public String get(int idx) { return instructions.get(idx); }
}