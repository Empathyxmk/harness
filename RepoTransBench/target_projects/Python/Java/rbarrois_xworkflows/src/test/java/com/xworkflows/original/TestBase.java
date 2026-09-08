package com.xworkflows.original;

import com.xworkflows.base.MinimalWorkflow;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestBase {

    public static class State {
        public final String name;
        public final String title;
        public State(String name, String title) { this.name=name; this.title=title; }
        @Override public boolean equals(Object obj) {
            if (obj == this) return true;
            if (!(obj instanceof State)) return false;
            State s = (State) obj;
            return this.name.equals(s.name) && this.title.equals(s.title);
        }
        @Override public int hashCode() { return Objects.hash(name, title); }
        @Override public String toString() { return name; }
    }

    public static class StateList extends ArrayList<State> {
        public StateList(List<State> items) { super(items); }
        public State getByName(String n) {
            for (State s : this) if (s.name.equals(n)) return s;
            throw new NoSuchElementException();
        }
    }

    public static class Transition {
        public final String name;
        public final List<State> source;
        public final State target;
        public Transition(String name, List<State> src, State tgt) {
            this.name = name; this.source = src; this.target = tgt;
        }
    }

    public static class TransitionList extends ArrayList<Transition> {
        public TransitionList(List<Transition> items) { super(items); }
        public Transition getByName(String n) {
            for (Transition t : this) if (t.name.equals(n)) return t;
            throw new NoSuchElementException();
        }
    }

    State foo;
    State bar;
    State baz;
    State bar2;
    StateList sl;
    Transition foobar;
    Transition foobar2;
    Transition gobaz;
    State baz2;
    TransitionList tl;

    @BeforeEach
    public void setup() {
        foo = new State("foo", "Foo");
        bar = new State("bar", "Bar");
        bar2 = new State("bar", "Bar");
        baz = new State("baz", "Baz");
        sl = new StateList(Arrays.asList(foo, bar));
        foobar = new Transition("foobar", List.of(foo), bar);
        foobar2 = new Transition("foobar", List.of(foo), bar);
        gobaz = new Transition("gobaz", List.of(foo, bar), baz);
        baz2 = new State("baz", "Baz");
        tl = new TransitionList(Arrays.asList(foobar, gobaz));
    }

    @Test
    public void testStateDefinition() {
        assertThrows(IllegalArgumentException.class, () -> {
            new State("a--b", "A--B");
        });
    }
    @Test
    public void testStateEquality() {
        assertNotEquals(new State("foo", "Foo"), new State("foo", "Foo"));
    }
    @Test
    public void testStateRepr() {
        State a = new State("foo", "Foo");
        assertTrue(a.toString().contains("foo"));
        assertFalse(a.toString().contains("Foo"));
    }
    @Test
    public void testStateListAccess() {
        assertEquals(foo, sl.get(0));
        assertEquals(foo, sl.getByName("foo"));
        assertThrows(NoSuchElementException.class, () -> sl.getByName("baz"));
    }
    @Test
    public void testStateListContains() {
        assertTrue(sl.contains(foo));
        assertTrue(sl.contains(bar));
        assertFalse(sl.contains(bar2));
        assertTrue(sl.getByName("foo").equals(foo));
        assertThrows(NoSuchElementException.class, () -> sl.getByName("bar2"));
    }
    @Test
    public void testStateListMethods() {
        assertTrue(!sl.isEmpty());
        assertTrue(new StateList(List.of()).isEmpty());
        assertEquals(2, sl.size());
    }
    @Test
    public void testTransitionListAccessAndMethods() {
        assertEquals(foobar, tl.get(0));
        assertEquals(foobar, tl.getByName("foobar"));
        assertThrows(NoSuchElementException.class, () -> tl.getByName("foobaz"));
        assertTrue(tl.contains(foobar));
        assertTrue(tl.contains(gobaz));
        assertFalse(tl.contains(foobar2));
        assertTrue(!tl.isEmpty());
        assertTrue(new TransitionList(List.of()).isEmpty());
        assertEquals(2, tl.size());
    }

    @Test
    public void testTransitionListAvailableFrom() {
        List<Transition> expected = List.of(foobar, gobaz);
        List<Transition> available = new ArrayList<>();
        for (Transition t : tl) {
            for (State s : t.source) {
                if (s.equals(foo)) { available.add(t); break; }
            }
        }
        assertEquals(expected, available);
    }

    @Test
    public void testTransitionListAvailableFromBarAndBaz() {
        List<Transition> available = new ArrayList<>();
        for (Transition t : tl) {
            for (State s : t.source) {
                if (s.equals(bar)) { available.add(t); break; }
            }
        }
        assertEquals(List.of(gobaz), available);

        List<Transition> availableBaz = new ArrayList<>();
        for (Transition t : tl) {
            for (State s : t.source) {
                if (s.equals(baz)) { availableBaz.add(t); break; }
            }
        }
        assertEquals(List.of(), availableBaz);
    }
}