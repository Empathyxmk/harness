package com.mapio.gvanim.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicTestActionExtra {
    static class DummyStep {
        public Set<Integer> V = new HashSet<>();
        public Set<Pair> E = new HashSet<>();
        public Map<Integer, String> lV = new HashMap<>();
        public Map<Pair, String> lE = new HashMap<>();
        public Map<Integer, String> hV = new HashMap<>();
        public Map<Pair, String> hE = new HashMap<>();
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
    void testAddNodeActionPublic() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        AddNode(12).apply(s);
        assertTrue(s.get(s.size()-1).V.contains(12));
    }

    @Test
    void testHighlightNodeAndLabelNodePublic() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        HighlightNode(20, "red").apply(s);
        LabelNode(20, "lbl2").apply(s);
        assertTrue(s.get(s.size()-1).hV.containsKey(20)
            && s.get(s.size()-1).lV.containsKey(20));
    }

    @Test
    void testUnlabelAndRemoveNodePublic() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        AddNode(9).apply(s);
        LabelNode(9, "zzz").apply(s);
        UnlabelNode(9).apply(s);
        assertFalse(s.get(s.size()-1).lV.containsKey(9));
        RemoveNode(9).apply(s);
        assertFalse(s.get(s.size()-1).V.contains(9));
    }

    @Test
    void testAddEdgeAndHighlightLabelUnlabelRemovePublic() {
        List<DummyStep> s = new ArrayList<>();
        s.add(new DummyStep());
        AddNode(6).apply(s);
        AddNode(13).apply(s);
        AddEdge(6, 13).apply(s);
        HighlightEdge(6, 13, "purple").apply(s);
        LabelEdge(6, 13, "Y").apply(s);
        assertTrue(s.get(s.size()-1).E.contains(new Pair(6, 13)) &&
            s.get(s.size()-1).hE.containsKey(new Pair(6, 13)) &&
            s.get(s.size()-1).lE.containsKey(new Pair(6, 13)));
        UnlabelEdge(6, 13).apply(s);
        RemoveEdge(6, 13).apply(s);
        assertFalse(s.get(s.size()-1).E.contains(new Pair(6, 13)));
    }
}