package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicPythonflowTest {

    static class Adder {
        final int x, y;
        Adder(int x, int y) { this.x = x; this.y = y; }
        int eval() { return x + y; }
    }

    @Test
    public void testPublicEval() {
        Adder adder = new Adder(11, 7);
        assertEquals(18, adder.eval());
    }
}