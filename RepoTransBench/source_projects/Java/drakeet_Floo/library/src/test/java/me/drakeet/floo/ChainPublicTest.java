package me.drakeet.floo;

import org.junit.Test;

import static org.junit.Assert.*;

public class ChainPublicTest {

    @Test
    public void testProceedReturnsData_public() {
        Chain<String> chain = new Chain<String>() {
            @Override
            public String proceed(String input) {
                return input + "_public";
            }
        };
        String result = chain.proceed("hello");
        assertEquals("hello_public", result);
    }

    @Test
    public void testProceedWithDifferentData_public() {
        Chain<Integer> chain = new Chain<Integer>() {
            @Override
            public Integer proceed(Integer input) {
                return input + 42;
            }
        };
        Integer result = chain.proceed(8);
        assertEquals(Integer.valueOf(50), result);
    }
}