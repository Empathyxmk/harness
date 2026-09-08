package com.ecmwf.ai_models.public_tests;

import org.junit.jupiter.api.Test;
import com.ecmwf.ai_models.code.SimpleCodeUtil;

class PublicCodeTest {

    @Test
    void test_public_code_math_ops() {
        int x = 3, y = 9;
        org.junit.jupiter.api.Assertions.assertEquals(27, SimpleCodeUtil.multiply(x, y));
        org.junit.jupiter.api.Assertions.assertEquals(3.0, SimpleCodeUtil.sqrt(y), 1e-9);
    }

    @Test
    void test_public_code_string_reverse() {
        String s = "abcdef";
        org.junit.jupiter.api.Assertions.assertEquals("fedcba", SimpleCodeUtil.reverse(s));
    }
}