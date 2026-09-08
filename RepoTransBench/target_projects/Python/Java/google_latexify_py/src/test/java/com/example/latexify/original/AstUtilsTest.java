package com.example.latexify.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AstUtilsTest {

    // Simulated AST node for testing deep copy, equality etc.
    static class AstNode {
        String type;
        Object value;

        AstNode(String type, Object value) {
            this.type = type;
            this.value = value;
        }

        AstNode deepCopy() {
            return new AstNode(this.type, this.value);
        }

        boolean astEquals(AstNode other) {
            if (other == null) return false;
            if (!type.equals(other.type)) return false;
            if (value == null && other.value != null) return false;
            if (value != null && other.value == null) return false;
            if (value == null && other.value == null) return true;
            return value.equals(other.value);
        }
    }

    @Test
    void testAstNodeEquality() {
        AstNode a = new AstNode("Num", 3);
        AstNode b = new AstNode("Num", 3);
        AstNode c = new AstNode("Num", 4);
        assertTrue(a.astEquals(b));
        assertFalse(a.astEquals(c));
    }

    @Test
    void testAstNodeDeepCopy() {
        AstNode a = new AstNode("Var", "x");
        AstNode copy = a.deepCopy();
        assertNotSame(a, copy);
        assertTrue(a.astEquals(copy));
    }
}