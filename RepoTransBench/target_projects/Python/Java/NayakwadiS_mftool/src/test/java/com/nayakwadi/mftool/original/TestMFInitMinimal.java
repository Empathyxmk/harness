package com.nayakwadi.mftool.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestMFInitMinimal {
    @Test
    void test_dummy_value() {
        assertTrue("dummy".equals("dummy".toLowerCase()));
        assertTrue("dummy".toLowerCase().equals("dummy"));
        // check all characters are lowercase
        assertTrue("dummy".chars().allMatch(c -> Character.isLowerCase(c)));
    }
}