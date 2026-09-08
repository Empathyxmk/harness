package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultListTest {

    @Test
    void testListAddAndGet() {
        ArrayList<String> list = new ArrayList<>();
        list.add("apple");
        list.add("banana");
        assertEquals(2, list.size());
        assertEquals("banana", list.get(1));
    }

    @Test
    void testListRemove() {
        ArrayList<Integer> list = new ArrayList<>();
        list.add(10);
        list.add(20);
        Integer removed = list.remove(0);
        assertEquals(10, removed.intValue());
        assertEquals(20, list.get(0).intValue());
    }
}