package com.xworkflows.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.lang.reflect.Field;
import java.util.*;

public class TestUsing {

    public static class State {
        public final String name;
        public final String title;
        public State(String name, String title) { this.name=name; this.title=title; }
        @Override public boolean equals(Object obj) {
            if (!(obj instanceof State)) return false;
            State s = (State)obj;
            return Objects.equals(name, s.name) && Objects.equals(title, s.title);
        }
        @Override public String toString() { return name; }
    }

    public static class Workflow {
        public final List<State> states;
        public final List<Transition> transitions;
        public final State initialState;
        public Workflow(State[] statesArr, Transition[] transitionsArr, String initialStateName) {
            this.states = Arrays.asList(statesArr);
            this.transitions = Arrays.asList(transitionsArr);
            State foundInit = null;
            for (State s : statesArr) { if (s.name.equals(initialStateName)) foundInit = s; }
            initialState = foundInit;
        }
    }

    public static class Transition {
        public final String name;
        public final List<State> source;
        public final State target;
        public Transition(String name, State[] src, State tgt) {
            this.name = name;
            this.source = Arrays.asList(src);
            this.target = tgt;
        }
    }

    public static Workflow makeWorkflowFooBarBaz() {
        State foo = new State("foo", "Foo");
        State bar = new State("bar", "Bar");
        State baz = new State("baz", "Baz");
        Transition foobar = new Transition("foobar", new State[]{foo}, bar);
        Transition gobaz = new Transition("gobaz", new State[]{foo, bar}, baz);
        Transition bazbar = new Transition("bazbar", new State[]{baz}, bar);
        return new Workflow(
                new State[]{foo, bar, baz},
                new Transition[]{foobar, gobaz, bazbar},
                "foo"
        );
    }

    @Test
    public void testSimpleDefinition() {
        Workflow wf = makeWorkflowFooBarBaz();
        assertEquals(3, wf.states.size());
        assertEquals(3, wf.transitions.size());
        assertEquals("foo", wf.initialState.name);
        State foo = wf.states.get(0);
        assertEquals("Foo", foo.title);
        assertTrue(foo.name.equals("foo") || foo.name.equals("bar") || foo.name.equals("baz"));
    }

    @Test
    public void testInvalidDefinitions_TypeError() {
        assertThrows(ClassCastException.class, () -> {
            Object[] states = {12, 13, 14};
            new Workflow((State[])states, new Transition[]{}, "12");
        });
    }

    @Test
    public void testInvalidDefinitions_KeyError() {
        assertThrows(NullPointerException.class, () -> {
            State foo = new State("foo", "Foo");
            State bar = new State("bar", "Bar");
            State baz = new State("baz", "Baz");
            Transition foobar = new Transition("foobar", new State[]{new State("bbb", "BBB")}, bar);
            new Workflow(
                    new State[]{foo, bar, baz},
                    new Transition[]{foobar},
                    "foo"
            );
        });
    }

    @Test
    public void testInvalidDefinitions_TypeError2() {
        assertThrows(ArrayStoreException.class, () -> {
            Object[] states = { new Object[]{1,2,3}, new Object[]{2,3,4} };
            new Workflow((State[]) states, new Transition[]{}, "12");
        });
    }
}