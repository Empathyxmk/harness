package com.initstring.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.*;
import java.util.stream.Stream;

import com.initstring.linkedin2username.NameMutator;

public class TestNamemutator {

    private static Stream<org.junit.jupiter.params.provider.Arguments> cleanAndSplitNameProvider() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of("John Smith", Map.of("first", "john", "last", "smith", "second", "")),
            org.junit.jupiter.params.provider.Arguments.of("Jane D'oe", Map.of("first", "jane", "last", "doe", "second", "")),
            org.junit.jupiter.params.provider.Arguments.of("Dr. Ángela Gómez (MBA, PhD)", Map.of("first", "angela", "last", "gomez", "second", "")),
            org.junit.jupiter.params.provider.Arguments.of("José Niño", Map.of("first", "jose", "last", "nino", "second", "")),
            org.junit.jupiter.params.provider.Arguments.of("Joe (CTO) Bloggs", Map.of("first", "joe", "last", "bloggs", "second", ""))
        );
    }

    @ParameterizedTest
    @MethodSource("cleanAndSplitNameProvider")
    public void testCleanAndSplitName(String input, Map<String, String> expected) {
        NameMutator nm = new NameMutator(input);
        assertEquals(expected, nm.name);
    }
}