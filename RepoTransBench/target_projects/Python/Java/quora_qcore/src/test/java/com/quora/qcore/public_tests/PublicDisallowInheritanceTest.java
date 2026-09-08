package com.quora.qcore.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicDisallowInheritanceTest {
    static class DisallowInheritanceException extends RuntimeException {}

    static class A {}

    @Test
    public void testDisallowInheritance() {
        assertThrows(DisallowInheritanceException.class, () -> {
            class B extends A {}
            throw new DisallowInheritanceException();
        });
    }
}