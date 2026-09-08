package me.ele.amigo.utils;

import org.junit.Test;
import static org.junit.Assert.*;

public class ArrayUtilPublicTest {

    @Test
    public void publicTestIsEmptyPublic() {
        Integer[] emptyArr = {};
        Integer[] nonEmptyArr = {456, 789};
        assertTrue(ArrayUtil.isEmpty(emptyArr));
        assertFalse(ArrayUtil.isEmpty(nonEmptyArr));
    }

    @Test
    public void publicTestConcatDiff() {
        Integer[] a = {2, 4};
        Integer[] b = {8, 16};
        Integer[] result = ArrayUtil.concat(a, b);
        assertArrayEquals(new Integer[]{2, 4, 8, 16}, result);
    }
}