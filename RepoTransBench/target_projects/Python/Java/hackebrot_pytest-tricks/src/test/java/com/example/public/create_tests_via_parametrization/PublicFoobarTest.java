package com.example.public.create_tests_via_parametrization;

import com.example.create_tests_via_parametrization.Foobar.Man;
import com.example.create_tests_via_parametrization.Foobar.Package;
import com.example.create_tests_via_parametrization.Foobar.Woman;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.Arguments;

import java.util.List;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

class PublicFoobarTest {

    public static List<Package> PUBLIC_PACKAGES = List.of(
            new Package("matplotlib", ""),
            new Package("pandas", "")
    );

    static Stream<Arguments> publicPythonPackageProvider() {
        return PUBLIC_PACKAGES.stream().map(Arguments::of);
    }

    static Stream<Arguments> becomeProgrammerProvider() {
        return Stream.of(
                Arguments.of(new Man("Oliver")),
                Arguments.of(new Woman("Amelia")),
                Arguments.of(new Man("Mason")),
                Arguments.of(new Man("Logan")),
                Arguments.of(new Woman("Harper"))
        );
    }

    static Stream<Arguments> learnMultiplePackagesProvider() {
        return Stream.of(
                Arguments.of(new Man("Jack")),
                Arguments.of(new Woman("Lily"))
        );
    }

    static Stream<Arguments> notProgrammerInitiallyProvider() {
        return Stream.of(
                Arguments.of(new Man("Henry")),
                Arguments.of(new Woman("Ella"))
        );
    }

    @ParameterizedTest
    @MethodSource("becomeProgrammerProvider")
    void testBecomeAProgrammerPublic(Object person) {
        for (Package pkg : PUBLIC_PACKAGES) {
            if (person instanceof Man) ((Man) person).learn(pkg.name);
            else if (person instanceof Woman) ((Woman) person).learn(pkg.name);
            assertThat(
                person instanceof Man
                    ? ((Man) person).looksLikeAProgrammer
                    : ((Woman) person).looksLikeAProgrammer
            ).isTrue();
        }
    }

    @ParameterizedTest
    @MethodSource("learnMultiplePackagesProvider")
    void testLearnMultiplePackagesPublic(Object person) {
        if (person instanceof Man) {
            ((Man) person).learn("sqlalchemy");
            ((Man) person).learn("httpx");
            assertThat(((Man) person).looksLikeAProgrammer).isTrue();
        }
        else if (person instanceof Woman) {
            ((Woman) person).learn("sqlalchemy");
            ((Woman) person).learn("httpx");
            assertThat(((Woman) person).looksLikeAProgrammer).isTrue();
        }
    }

    @ParameterizedTest
    @MethodSource("notProgrammerInitiallyProvider")
    void testNotProgrammerInitiallyPublic(Object person) {
        assertThat(
            person instanceof Man
                ? ((Man) person).looksLikeAProgrammer
                : ((Woman) person).looksLikeAProgrammer
        ).isFalse();
    }
}