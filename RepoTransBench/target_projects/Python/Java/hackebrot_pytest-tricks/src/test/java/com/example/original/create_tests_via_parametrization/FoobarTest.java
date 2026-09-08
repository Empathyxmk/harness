package com.example.original.create_tests_via_parametrization;

import com.example.create_tests_via_parametrization.Foobar.Man;
import com.example.create_tests_via_parametrization.Foobar.Package;
import com.example.create_tests_via_parametrization.Foobar.Woman;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.Arguments;

import java.util.List;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

class FoobarTest {

    public static List<Package> PACKAGES = List.of(
            new Package("requests", "Apache 2.0"),
            new Package("django", "BSD"),
            new Package("pytest", "MIT")
    );

    static Stream<Arguments> pythonPackageProvider() {
        return PACKAGES.stream().map(Arguments::of);
    }

    static Stream<Arguments> peopleProvider() {
        return Stream.of(
                Arguments.of(new Woman("Audrey")),
                Arguments.of(new Woman("Brianna")),
                Arguments.of(new Man("Daniel")),
                Arguments.of(new Woman("Ola")),
                Arguments.of(new Man("Kenneth"))
        );
    }

    @ParameterizedTest
    @MethodSource("peopleProvider")
    void testBecomeAProgrammer(Object person) {
        // For every package, the person must look like a programmer after learning it
        for (Package pkg : PACKAGES) {
            if (person instanceof Man) ((Man) person).learn(pkg.name);
            else if (person instanceof Woman) ((Woman) person).learn(pkg.name);
            // After learning, should look like a programmer
            assertThat((person instanceof Man ? ((Man) person).looksLikeAProgrammer : ((Woman) person).looksLikeAProgrammer)).isTrue();
        }
    }

    @ParameterizedTest
    @MethodSource("pythonPackageProvider")
    void testIsOpenSource(Package pkg) {
        assertThat(pkg.isOpenSource()).isTrue();
    }
}