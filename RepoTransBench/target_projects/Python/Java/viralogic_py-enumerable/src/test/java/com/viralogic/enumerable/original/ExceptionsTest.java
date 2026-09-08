package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ExceptionsTest {

    @Test
    void testThrowsIndexOutOfBounds() {
        assertThrows(IndexOutOfBoundsException.class, () -> {
            List<Integer> list = new java.util.ArrayList<>();
            list.get(0); // should throw
        });
    }

    @Test
    void testNoSuchElementThrows() {
        assertThrows(NoSuchElementException.class, () -> {
            Iterator<Integer> it = new java.util.ArrayList<Integer>().iterator();
            it.next();
        });
    }
}