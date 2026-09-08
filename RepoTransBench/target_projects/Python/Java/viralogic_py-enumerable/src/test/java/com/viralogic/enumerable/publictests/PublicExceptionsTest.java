package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicExceptionsTest {

    @Test
    void testOutOfBoundsPublic() {
        List<String> l = Collections.emptyList();
        assertThrows(IndexOutOfBoundsException.class, () -> {
            l.get(2);
        });
    }

    @Test
    void testNoSuchElementPublic() {
        Iterator<Integer> empty = Collections.emptyIterator();
        assertThrows(NoSuchElementException.class, empty::next);
    }
}