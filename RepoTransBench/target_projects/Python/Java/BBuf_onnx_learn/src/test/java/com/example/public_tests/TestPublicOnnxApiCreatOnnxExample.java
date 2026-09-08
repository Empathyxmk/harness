package com.example.public_tests;

import com.example.onnxapi.CreatOnnxExample;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicOnnxApiCreatOnnxExample {

    @Test
    void testMakeIdentity() {
        assertEquals("hello", CreatOnnxExample.makeIdentity("hello"));
        assertEquals(Arrays.asList(7, 8, 9), CreatOnnxExample.makeIdentity(Arrays.asList(7, 8, 9)));
    }

    @Test
    void testSumList() {
        assertEquals(15, CreatOnnxExample.sumList(Arrays.asList(4, 5, 6)));
        assertEquals(100, CreatOnnxExample.sumList(Arrays.asList(100)));
    }
}