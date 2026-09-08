package com.example.publictests.api.v1;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicCasbinTest {
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
        policies.add(new Policy("public", "/api/v1/public", "get"));
    }

    @Test
    void testHasPublicPolicy() {
        Policy p = new Policy("public", "/api/v1/public", "get");
        assertTrue(policies.contains(p), "Should contain the public get policy");
    }

    @Test
    void testAddPublicPolicy() {
        Policy newp = new Policy("user", "/api/v1/public", "post");
        policies.add(newp);
        assertTrue(policies.contains(newp));
    }
}