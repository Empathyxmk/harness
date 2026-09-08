package com.example.public.create_tests_via_parametrization;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.assertj.core.api.Assertions.assertThat;

import java.util.stream.Stream;

class PublicParametrizeTest {

    static final Object[][] PUBLIC_RULES = new Object[][]{
            {14, "FooBar"},
            {2, "Foo"},
            {7, "Bar"}
    };

    static String foobar(int number) {
        for (Object[] rule : PUBLIC_RULES) {
            int div = (int) rule[0];
            String subst = (String) rule[1];
            if (number % div == 0) return subst;
        }
        return Integer.toString(number);
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> foobarProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of(1, "1"),
                org.junit.jupiter.params.provider.Arguments.of(2, "Foo"),
                org.junit.jupiter.params.provider.Arguments.of(7, "Bar"),
                org.junit.jupiter.params.provider.Arguments.of(14, "FooBar"),
                org.junit.jupiter.params.provider.Arguments.of(8, "Foo"),
                org.junit.jupiter.params.provider.Arguments.of(13, "13")
        );
    }

    @ParameterizedTest
    @MethodSource("foobarProvider")
    void testFoobar(int number, String word) {
        assertThat(foobar(number)).isEqualTo(word);
    }
}