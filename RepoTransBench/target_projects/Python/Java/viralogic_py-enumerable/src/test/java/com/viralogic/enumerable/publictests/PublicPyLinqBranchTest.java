package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.Collectors;

class PublicPyLinqBranchTest {

    @Test
    void testBranchPublic() {
        List<String> all = Arrays.asList("a","b","c","d");
        List<String> firstTwo = all.stream().limit(2).collect(Collectors.toList());
        List<String> rest = all.stream().skip(2).collect(Collectors.toList());
        assertEquals(Arrays.asList("a","b"), firstTwo);
        assertEquals(Arrays.asList("c","d"), rest);
    }
}