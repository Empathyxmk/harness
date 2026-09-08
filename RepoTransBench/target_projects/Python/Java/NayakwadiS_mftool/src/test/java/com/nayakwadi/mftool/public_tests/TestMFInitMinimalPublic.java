package com.nayakwadi.mftool.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestMFInitMinimalPublic {
    @Test
    void test_dummy_value_public() {
        assertFalse("DUMMY".equals("DUMMY".toLowerCase()));
        assertFalse("DUMMY".toLowerCase().equals("DUMMY"));
        assertFalse("DUMMY".chars().allMatch(c -> Character.isLowerCase(c)));
    }
}