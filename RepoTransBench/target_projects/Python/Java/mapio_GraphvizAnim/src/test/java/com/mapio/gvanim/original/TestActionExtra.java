package com.mapio.gvanim.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class TestActionExtra {

    static class DummyStep {
        public Set<Integer> V = new HashSet<>();
        public Set<Pair> E = new HashSet<>();
        public Map<Integer, String> lV = new HashMap<>();
        public Map<Pair, String> lE = new HashMap<>();
        public Map<Integer, String> hV = new HashMap<>();
        public Map<Pair, String> hE = new HashMap<>();

        public DummyStep() {}
    }
    static class Pair {
        public int a, b;
        public Pair(int a, int b) { this.a = a; this.b = b; }
        @Override public boolean equals(Object o) {
            if (!(o instanceof Pair)) return false;
            Pair p = (Pair) o;
            return a == p.a && b == p.b;
        }
        @Override public int hashCode() { return Objects.hash(a, b); }
    }
    // Simulate action classes as lambdas
    interface StepAction { void apply(List<DummyStep> s); }
    static StepAction AddNode(int n) {
        return (List<DummyStep> s) -> s.get(s.size()-1).V.add(n);
    }
    static StepAction HighlightNode(int n, String color) {
        return (List<DummyStep> s) -> s.get(s.size()-1).hV.put(n, color);
    }
    static StepAction LabelNode(int n, String lbl) {
        return (List<DummyStep> s) -> s.get(s.size()-1).lV.put(n, lbl);
    }
    static StepAction UnlabelNode(int n) {
        return (List<DummyStep> s) -> s.get(s.size()-1).lV.remove(n);
    }
    static StepAction RemoveNode(int n) {
        return (List<DummyStep> s) -> s.get(s.size()-1).V.remove(n);
    }
    static StepAction AddEdge(int a, int b) {
        return (List<DummyStep> s) -> s.get(s.size()-1).E.add(new Pair(a, b));
    }
    static StepAction HighlightEdge(int a, int b, String color) {
        return (List<DummyStep> s) -> s.get(s.size()-1).hE.put(new Pair(a, b), color);
    }
    static StepAction LabelEdge(int a, int b, String lbl) {
        return (List<DummyStep> s) -> s.get(s.size()-1).lE.put(new Pair(a, b), lbl);
    }
    static StepAction UnlabelEdge(int a, int b) {
        return (List<DummyStep> s) -> s.get(s.size()-1).lE.remove(new Pair(a, b));
    }
    static StepAction RemoveEdge(int a, int b) {
        return (List<DummyStep> s) -> s.get(s.size()-1).E.remove(new Pair(a, b));
    }

    @Test
    void testAddNodeAction() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        AddNode(42).apply(s);
        assertTrue(s.get(s.size()-1).V.contains(42));
    }
    @Test
    void testHighlightNodeAndLabelNode() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        HighlightNode(2, "blue").apply(s);
        LabelNode(2, "lbl").apply(s);
        assertTrue(s.get(s.size()-1).hV.containsKey(2) &&
                   s.get(s.size()-1).lV.containsKey(2));
    }
    @Test
    void testUnlabelAndRemoveNode() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        AddNode(1).apply(s);
        LabelNode(1, "tok").apply(s);
        UnlabelNode(1).apply(s);
        assertFalse(s.get(s.size()-1).lV.containsKey(1));
        RemoveNode(1).apply(s);
        assertFalse(s.get(s.size()-1).V.contains(1));
    }
    @Test
    void testAddEdgeAndHighlightLabelUnlabelRemove() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        AddNode(3).apply(s);
        AddNode(4).apply(s);
        AddEdge(3, 4).apply(s);
        HighlightEdge(3, 4, "green").apply(s);
        LabelEdge(3, 4, "X").apply(s);
        assertTrue(s.get(s.size()-1).E.contains(new Pair(3, 4))
                   && s.get(s.size()-1).hE.containsKey(new Pair(3, 4))
                   && s.get(s.size()-1).lE.containsKey(new Pair(3, 4)));
        UnlabelEdge(3, 4).apply(s);
        RemoveEdge(3, 4).apply(s);
        assertFalse(s.get(s.size()-1).E.contains(new Pair(3, 4)));
    }
}