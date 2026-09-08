package com.nickjj.publictests;

import com.nickjj.logic.DummyLogic;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class PublicDummyLogicTest {
    @Test
    void testIncrementPublic() {
        assertEquals(11, DummyLogic.increment(10));
        assertEquals(-3, DummyLogic.increment(-4));
    }

    @Test
    void testSumPublic() {
        assertEquals(23, DummyLogic.total(Arrays.asList(3, 8, 12)));
        assertEquals(0, DummyLogic.total(Collections.emptyList()));
        assertEquals(3, DummyLogic.total(Arrays.asList(-2, 5)));
    }

    @Test
    void testIsEvenPublic() {
        assertTrue(DummyLogic.isEven(100));
        assertFalse(DummyLogic.isEven(15));
        assertTrue(DummyLogic.isEven(-22));
    }

    @Test
    void testCustomCasePublic() {
        int[] numbers = {6, 7, 8, 9};
        int evenCount = 0;
        for (int n : numbers) {
            if (DummyLogic.isEven(n)) evenCount++;
        }
        assertEquals(2, evenCount);
    }

    @Test
    void testZeroIncrementPublic() {
        assertEquals(1, DummyLogic.increment(0));
    }

    @Test
    void testNegativeTotalPublic() {
        assertEquals(-20, DummyLogic.total(Arrays.asList(-5, -5, -10)));
    }
}