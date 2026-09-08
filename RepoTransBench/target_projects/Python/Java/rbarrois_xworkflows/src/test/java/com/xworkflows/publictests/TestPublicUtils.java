package com.xworkflows.publictests;

import com.xworkflows.utils.IterclassUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

public class TestPublicUtils {

    @Test
    public void testIterclassTraversalDifferent() {
        class C {
            public static int x = 10;
        }
        class D extends C {
            public static int y = 20;
        }
        Map<String, Object> result = IterclassUtils.iterclass(D.class);
        assertEquals(10, result.get("x"));
        assertEquals(20, result.get("y"));
    }

    @Test
    public void testIterclassOverridesDifferent() {
        class C {
            public static int alpha = 7;
        }
        class D extends C {
            public static int alpha = 42;
        }
        Map<String, Object> result = IterclassUtils.iterclass(D.class);
        assertEquals(42, result.get("alpha"));
    }
}