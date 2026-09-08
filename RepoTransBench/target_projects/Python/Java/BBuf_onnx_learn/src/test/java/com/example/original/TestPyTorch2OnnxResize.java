package com.example.original;

import com.example.convert2onnx.PyTorch2OnnxResize;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPyTorch2OnnxResize {

    @Test
    void testDummyResizeFunc() {
        PyTorch2OnnxResize.Pair<Integer, Integer> out = PyTorch2OnnxResize.dummyResizeFunc(4, 5);
        assertEquals(new PyTorch2OnnxResize.Pair<>(4, 5), out);

        PyTorch2OnnxResize.Pair<String, Integer> out2 = PyTorch2OnnxResize.dummyResizeFunc("x", 42);
        assertEquals(new PyTorch2OnnxResize.Pair<>("x", 42), out2);
    }
}