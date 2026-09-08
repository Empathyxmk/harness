package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class FunctionsTest {
    @Test
    void testOnce() {
        List<Integer> called = new ArrayList<>();
        Underscore.SupplierOnce<Integer> func = new Underscore.SupplierOnce<Integer>() {
            @Override
            public Integer get() {
                called.add(1);
                return 3;
            }
        };
        Underscore.SupplierOnce<Integer> onceFunc = Underscore.once(func);
        assertEquals(3, (int) onceFunc.get());
        onceFunc.get();
        assertEquals(Collections.singletonList(1), called);
    }
}