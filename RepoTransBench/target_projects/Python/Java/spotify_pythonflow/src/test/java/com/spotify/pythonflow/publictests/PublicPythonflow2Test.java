package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicPythonflow2Test {

    static class Identity {
        final int x;
        Identity(int x) { this.x = x; }
        int eval() { return x; }
    }

    @Test
    public void testPublicEvalIdentity() {
        Identity i = new Identity(13);
        assertEquals(13, i.eval());
    }
}