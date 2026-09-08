package com.initstring.public_;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import com.initstring.linkedin2username.NameMutator;

import java.util.*;
import java.util.stream.Stream;

public class TestPublicNamemutator {

    private static Stream<org.junit.jupiter.params.provider.Arguments> publicProvider() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of("Sam Lee", Map.of("first","sam","last","lee","second","")),
            org.junit.jupiter.params.provider.Arguments.of("Ms. Eva O'Brien", Map.of("first","eva","last","obrien","second","")),
            org.junit.jupiter.params.provider.Arguments.of("Prof. Łukasz Nowak (PhD)", Map.of("first","lukasz","last","nowak","second","")),
            org.junit.jupiter.params.provider.Arguments.of("María-José Carreño", Map.of("first","maria","last","carreno","second","")),
            org.junit.jupiter.params.provider.Arguments.of("Chris (CEO) Smithers", Map.of("first", "chris", "last", "smithers", "second", ""))
        );
    }

    @ParameterizedTest
    @MethodSource("publicProvider")
    public void testCleanAndSplitNamePublic(String input, Map<String,String> expected) {
        NameMutator nm = new NameMutator(input);
        assertEquals(expected, nm.name);
    }
}