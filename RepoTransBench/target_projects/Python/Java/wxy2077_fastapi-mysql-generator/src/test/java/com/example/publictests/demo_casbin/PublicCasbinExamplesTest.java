package com.example.publictests.demo_casbin;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicCasbinExamplesTest {

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

    static class Enforcer {
        Set<Policy> pols = new HashSet<>();
        Enforcer() {}
        Enforcer addPolicy(String s, String o, String a) { pols.add(new Policy(s,o,a)); return this; }
        boolean enforce(String s, String o, String a) { return pols.contains(new Policy(s,o,a)); }
    }

    @Test
    void testPublicDemoPolicy() {
        Enforcer e = new Enforcer();
        e.addPolicy("guest", "pubdata", "read");
        assertTrue(e.enforce("guest", "pubdata", "read"), "guest can read pubdata");
        assertFalse(e.enforce("guest", "pubdata", "write"), "guest can't write pubdata");
    }
}