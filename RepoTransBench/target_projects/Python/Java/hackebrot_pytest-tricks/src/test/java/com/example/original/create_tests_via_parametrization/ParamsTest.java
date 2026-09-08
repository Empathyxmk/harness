package com.example.original.create_tests_via_parametrization;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class ParamsTest {
    @ParameterizedTest
    @ValueSource(strings = {"apple", "banana"})
    void testFruit(String fruit) {
        // Always passes
        assert true;
    }
}