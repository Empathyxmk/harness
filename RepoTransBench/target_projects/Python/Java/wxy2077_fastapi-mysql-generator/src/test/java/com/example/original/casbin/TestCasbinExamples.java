package com.example.original.casbin;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestCasbinExamples {

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
        Set<Policy> policySet = new HashSet<>();
        void addPolicy(String s, String o, String a) {
            policySet.add(new Policy(s, o, a));
        }
        boolean enforce(String s, String o, String a) {
            return policySet.contains(new Policy(s, o, a));
        }
        boolean removePolicy(String s, String o, String a) {
            return policySet.remove(new Policy(s, o, a));
        }
        int policyCount() {
            return policySet.size();
        }
    }

    Enforcer enforcer;

    @BeforeEach
    void setup() {
        enforcer = new Enforcer();
        enforcer.addPolicy("alice", "data1", "read");
        enforcer.addPolicy("bob", "data2", "write");
    }

    @Test
    void testEnforcePolicy() {
        assertTrue(enforcer.enforce("alice", "data1", "read"));
        assertFalse(enforcer.enforce("alice", "data2", "write"));
    }

    @Test
    void testAddPolicy() {
        enforcer.addPolicy("eve", "data3", "read");
        assertTrue(enforcer.enforce("eve", "data3", "read"));
    }

    @Test
    void testRemovePolicy() {
        boolean removed = enforcer.removePolicy("bob", "data2", "write");
        assertTrue(removed);
        assertFalse(enforcer.enforce("bob", "data2", "write"));
    }

    @Test
    void testPolicyCount() {
        assertEquals(2, enforcer.policyCount());
        enforcer.addPolicy("peter", "data4", "edit");
        assertEquals(3, enforcer.policyCount());
    }
}