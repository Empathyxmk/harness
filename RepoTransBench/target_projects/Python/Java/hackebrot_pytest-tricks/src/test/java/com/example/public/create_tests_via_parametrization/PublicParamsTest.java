package com.example.public.create_tests_via_parametrization;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class PublicParamsTest {
    @ParameterizedTest
    @ValueSource(strings = {"orange", "grape"})
    void testFruitPublic(String fruit) {
        assert true;
    }
}