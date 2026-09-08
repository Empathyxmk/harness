package com.manning.junitbook.ch02.parametrized;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertFalse;

class ParameterizedWithEnumSourcePublicTest {

    enum Colors {
        RED, GREEN, BLUE, YELLOW
    }

    boolean isPrimary(Colors color) {
        return color == Colors.RED || color == Colors.GREEN || color == Colors.BLUE;
    }

    @ParameterizedTest
    @EnumSource(value = Colors.class, names = {"RED", "BLUE"})
    void testIsPrimaryTrue(Colors color) {
        assertTrue(isPrimary(color), color + " should be primary");
    }

    @ParameterizedTest
    @EnumSource(value = Colors.class, names = {"YELLOW"})
    void testIsPrimaryFalse(Colors color) {
        assertFalse(isPrimary(color), color + " should not be primary");
    }
}