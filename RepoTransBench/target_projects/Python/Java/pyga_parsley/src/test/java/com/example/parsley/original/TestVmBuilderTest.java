package com.example.parsley.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestVmBuilderTest {

    @Test
    public void testVmBuildAddsInstructions() {
        VmBuilder builder = new VmBuilder();
        builder.add("LOAD 42");
        builder.add("RETURN");
        assertEquals(2, builder.instructionsCount());
        assertEquals("LOAD 42", builder.get(0));
        assertEquals("RETURN", builder.get(1));
    }
}

class VmBuilder {
    private final java.util.List<String> instructions = new java.util.ArrayList<>();
    public void add(String instr) { instructions.add(instr); }
    public int instructionsCount() { return instructions.size(); }
    public String get(int i) { return instructions.get(i); }
}