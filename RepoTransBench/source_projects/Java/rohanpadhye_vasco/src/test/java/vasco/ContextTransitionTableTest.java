package vasco;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

import java.util.Set;
import java.util.HashSet;

public class ContextTransitionTableTest {

    static class DummyContext extends Context<String, String, Integer> {
        private final int id;
        private final String methodName;

        DummyContext(String method, int id) {
            super(method, null, false);
            this.methodName = method;
            this.id = id;
        }
        @Override
        public int getId() { return id; }
        @Override
        public String getMethod() { return methodName; }
        @Override
        public boolean equals(Object obj) {
            if (!(obj instanceof DummyContext)) return false;
            DummyContext d = (DummyContext) obj;
            return id == d.id && methodName.equals(d.methodName);
        }
        @Override
        public int hashCode() { return id * 31 + methodName.hashCode(); }
    }

    private ContextTransitionTable<String, String, Integer> table;
    private DummyContext ctxA, ctxB;
    private CallSite<String, String, Integer> site1, site2;

    @Before
    public void setUp() {
        table = new ContextTransitionTable<>();
        ctxA = new DummyContext("foo", 1);
        ctxB = new DummyContext("bar", 2);
        site1 = new CallSite<>(ctxA, "node1");
        site2 = new CallSite<>(ctxB, "node2");
    }

    @Test
    public void testAddAndQueryTransitions() {
        // initially nothing
        assertFalse(table.hasCallers(ctxB));
        assertNull(table.getCalledContexts(site1, "bar"));

        table.addTransition(site1, ctxB);
        Set<Context<String,String,Integer>> called = table.getCalledContexts(site1);
        assertTrue(called.contains(ctxB));
        assertEquals(ctxB, table.getCalledContexts(site1, "bar"));
        assertTrue(table.hasCallers(ctxB));

        // Adding again with a different context for site2 and null target
        table.addTransition(site2, null); // default/unknown transition
        assertTrue(table.isDefaultCallSite(site2));
        assertTrue(table.getDefaultCallSites().contains(site2));
    }

    @Test
    public void testCallSitesOfContext() {
        // add call site to context
        table.addCallSiteToContext(ctxA, site1);
        Set<CallSite<String,String,Integer>> s = table.getCallSitesOfContext(ctxA);
        assertTrue(s.contains(site1));
    }

    @Test
    public void testGetCallers() {
        table.addTransition(site1, ctxB);
        Set<CallSite<String,String,Integer>> callers = table.getCallers(ctxB);
        assertTrue(callers.contains(site1));
    }
}