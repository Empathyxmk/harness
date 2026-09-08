package com.zaxxer.sansorm;

import org.junit.Test;

import static org.junit.Assert.*;

public class SqlFunctionPublicTest {

    @Test
    public void testApplyIntFunctionPublic() {
        // Using different input/output than existing tests
        SqlFunction<Integer, String> func = (v) -> "Num" + (v + 3);
        assertEquals("Num8", func.apply(5));
        assertEquals("Num12", func.apply(9));
    }

    @Test
    public void testApplyStringFunctionPublic() {
        // Different test data
        SqlFunction<String, Integer> func = (s) -> s.length() + 100;
        assertEquals(Integer.valueOf(104), func.apply("test"));
        assertEquals(Integer.valueOf(110), func.apply("abcdefghij"));
    }
}