package com.example.original.create_tests_via_parametrization;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

class ParametrizeTest {

    static final Object[][] RULES = new Object[][] {
            {15, "FizzBuzz"},
            {3, "Fizz"},
            {5, "Buzz"}
    };

    static String fizzbuzz(int number) {
        for (Object[] rule : RULES) {
            int divNumber = (Integer) rule[0];
            String subst = (String) rule[1];
            if (number % divNumber == 0) {
                return subst;
            }
        }
        return Integer.toString(number);
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> fizzbuzzProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of(1, "1"),
                org.junit.jupiter.params.provider.Arguments.of(3, "Fizz"),
                org.junit.jupiter.params.provider.Arguments.of(5, "Buzz"),
                org.junit.jupiter.params.provider.Arguments.of(10, "Buzz"),
                org.junit.jupiter.params.provider.Arguments.of(15, "FizzBuzz"),
                org.junit.jupiter.params.provider.Arguments.of(16, "16")
        );
    }

    @ParameterizedTest
    @MethodSource("fizzbuzzProvider")
    void testFizzBuzz(int number, String word) {
        assertThat(fizzbuzz(number)).isEqualTo(word);
    }
}