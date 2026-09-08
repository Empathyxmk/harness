package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicFunctionsTest {
    @Test
    void testOncePublic() {
        List<String> called = new ArrayList<>();
        Underscore.SupplierOnce<String> func = new Underscore.SupplierOnce<String>() {
            @Override
            public String get() {
                called.add("called");
                return "foo";
            }
        };
        Underscore.SupplierOnce<String> onceFunc = Underscore.once(func);
        assertEquals("foo", onceFunc.get());
        onceFunc.get();
        assertEquals(Collections.singletonList("called"), called);
    }
}