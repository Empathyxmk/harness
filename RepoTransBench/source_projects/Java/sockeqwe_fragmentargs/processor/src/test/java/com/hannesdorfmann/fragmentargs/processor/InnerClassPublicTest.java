package com.hannesdorfmann.fragmentargs.processor;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Public test for InnerClass handling with different test data.
 */
public class InnerClassPublicTest {

    @Test
    public void testInnerClassAccess_publicVariant() {
        OuterClassPublic outer = new OuterClassPublic(21);
        OuterClassPublic.InnerClass inner = outer.new InnerClass();
        // Use different data: multiply by 5, expect 105
        assertEquals(105, inner.multiplyOuterField(5));
    }

    static class OuterClassPublic {
        private int value;
        public OuterClassPublic(int value) {
            this.value = value;
        }
        public class InnerClass {
            public int multiplyOuterField(int by) {
                return value * by;
            }
        }
    }
}