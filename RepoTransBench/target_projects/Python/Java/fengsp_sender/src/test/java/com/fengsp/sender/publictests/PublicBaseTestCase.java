package com.fengsp.sender.publictests;

import org.junit.jupiter.api.Assertions;

public interface PublicBaseTestCase {

    default void setup() {}

    default void teardown() {}

    default void assert_equal(Object first, Object second) {
        Assertions.assertEquals(first, second);
    }

    default void assert_true(boolean expr, String msg) {
        Assertions.assertTrue(expr, msg);
    }

    default void assert_false(boolean expr, String msg) {
        Assertions.assertFalse(expr, msg);
    }

    default void assert_raises(Class<? extends Throwable> exception, Runnable callable) {
        Assertions.assertThrows(exception, callable::run);
    }

    default void assert_in(Object first, String second) {
        Assertions.assertTrue(second.contains(first.toString()));
    }

    default void assert_not_in(Object first, String second) {
        Assertions.assertFalse(second.contains(first.toString()));
    }

    default void assert_isinstance(Object obj, Class<?> cls) {
        Assertions.assertTrue(cls.isInstance(obj));
    }
}