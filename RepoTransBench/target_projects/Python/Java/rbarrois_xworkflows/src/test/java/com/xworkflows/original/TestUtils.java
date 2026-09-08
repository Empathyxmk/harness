package com.xworkflows.original;

import com.xworkflows.utils.IterclassUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

public class TestUtils {

    @Test
    public void testIterclassTraversal() {
        class A {
            public static int a = 1;
        }
        class B extends A {
            public static int b = 2;
        }

        Map<String, Object> result = IterclassUtils.iterclass(B.class);
        assertEquals(1, result.get("a"));
        assertEquals(2, result.get("b"));
    }

    @Test
    public void testIterclassOverrides() {
        class A {
            public static int foo = 3;
        }
        class B extends A {
            public static int foo = 4;
        }

        Map<String, Object> result = IterclassUtils.iterclass(B.class);
        assertEquals(4, result.get("foo"));
    }
}