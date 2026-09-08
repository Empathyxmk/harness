package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicCoreBasic2Test {

    @Test
    public void testPublicGraphContextEmpty() {
        Map<String, Integer> ctx = new HashMap<>();
        assertEquals(0, ctx.size());
    }
}