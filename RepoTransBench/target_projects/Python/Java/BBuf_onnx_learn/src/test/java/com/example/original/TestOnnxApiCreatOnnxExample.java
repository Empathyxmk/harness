package com.example.original;

import com.example.onnxapi.CreatOnnxExample;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class TestOnnxApiCreatOnnxExample {

    @Test
    void testMakeIdentity() {
        assertEquals(100, (int)CreatOnnxExample.makeIdentity(100));
        assertEquals(Arrays.asList(1, 2, 3), CreatOnnxExample.makeIdentity(Arrays.asList(1, 2, 3)));
    }

    @Test
    void testSumList() {
        assertEquals(6, CreatOnnxExample.sumList(Arrays.asList(1, 2, 3)));
        assertEquals(0, CreatOnnxExample.sumList(Collections.emptyList()));
    }
}