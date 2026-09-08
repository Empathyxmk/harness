package com.example.original.api.v1;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestCasbin {
    static class Policy {
        String sub, obj, act;
        Policy(String s, String o, String a) { sub=s; obj=o; act=a; }
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Policy)) return false;
            Policy p = (Policy)o;
            return sub.equals(p.sub) && obj.equals(p.obj) && act.equals(p.act);
        }
        @Override
        public int hashCode() { return Objects.hash(sub, obj, act); }
    }

    static Set<Policy> policies = new HashSet<>();

    @BeforeEach
    void setup() {
        policies.clear();
        policies.add(new Policy("alice", "data1", "read"));
        policies.add(new Policy("bob", "data2", "write"));
    }

    @Test
    void testHasPolicy() {
        assertTrue(policies.contains(new Policy("alice","data1","read")));
        assertFalse(policies.contains(new Policy("alice","data2","write")));
    }

    @Test
    void testAddPolicy() {
        Policy pol = new Policy("eve", "data3", "read");
        policies.add(pol);
        assertTrue(policies.contains(pol));
    }

    @Test
    void testRemovePolicy() {
        Policy toRemove = new Policy("bob", "data2", "write");
        policies.remove(toRemove);
        assertFalse(policies.contains(toRemove));
    }
}