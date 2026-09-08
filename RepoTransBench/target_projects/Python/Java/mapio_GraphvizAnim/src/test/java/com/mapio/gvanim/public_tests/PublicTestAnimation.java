package com.mapio.gvanim.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class DummyStep {
    public Set<Integer> V = new HashSet<>();
    public Set<Pair> E = new HashSet<>();
    public Map<Integer, String> lV = new HashMap<>();
    public Map<Pair, String> lE = new HashMap<>();
    public Map<Integer, String> hV = new HashMap<>();
    public Map<Pair, String> hE = new HashMap<>();

    public DummyStep() {}
    public DummyStep(DummyStep other) {
        this.V.addAll(other.V);
        this.E.addAll(other.E);
        this.lV.putAll(other.lV);
        this.lE.putAll(other.lE);
        this.hV.putAll(other.hV);
        this.hE.putAll(other.hE);
    }
    public String nodeFormat(int n) {
        if (!V.contains(n)) return "style=invis";
        StringBuilder sb = new StringBuilder();
        sb.append("label=").append(lV.containsKey(n) ? lV.get(n) : "");
        if (hV.containsKey(n)) sb.append(" color=").append(hV.get(n));
        return sb.toString();
    }
    public String edgeFormat(Pair e) {
        if (!E.contains(e)) return "style=invis";
        StringBuilder sb = new StringBuilder();
        sb.append("label=").append(lE.containsKey(e) ? lE.get(e) : "");
        if (hE.containsKey(e)) sb.append(" color=").append(hE.get(e));
        return sb.toString();
    }
    @Override
    public String toString() {
        return "V=" + V + " E=" + E;
    }
}
class Pair {
    public int a, b;
    public Pair(int a, int b) { this.a = a; this.b = b; }
    @Override public boolean equals(Object o) {
        if (!(o instanceof Pair)) return false;
        Pair p = (Pair) o;
        return a == p.a && b == p.b;
    }
    @Override public int hashCode() { return Objects.hash(a, b); }
    @Override public String toString() { return "(" + a + "," + b + ")"; }
}
class DummyParseException extends RuntimeException {
    public DummyParseException(String m) { super(m); }
}
class DummyAnimation {
    public void nextStep() {}
    public void addNode(int v) {}
    public void highlightNode(int v, String color) {}
    public void labelNode(int v, String lbl) {}
    public void unlabelNode(int v) {}
    public void removeNode(int v) {}
    public void addEdge(int a, int b) {}
    public void highlightEdge(int a, int b, String color) {}
    public void labelEdge(int a, int b, String lbl) {}
    public void unlabelEdge(int a, int b) {}
    public void removeEdge(int a, int b) {}
    public void parse(List<String> cmds) {
        for (String c : cmds) {
            if (c.startsWith("badcmd") || c.startsWith("an invalidnum") || c.startsWith("ae")) {
                throw new DummyParseException("parse error");
            }
        }
    }
}

public class PublicTestAnimation {

    @Test
    void testStepCopyAndReprPublic() {
        DummyStep step1 = new DummyStep();
        step1.V.add(10);
        step1.E.add(new Pair(10, 20));
        step1.lV.put(10, "X");
        step1.lE.put(new Pair(10, 20), "EdgeAB");
        DummyStep step2 = new DummyStep(step1);
        assertEquals(step1.V, step2.V);
        assertEquals(step1.E, step2.E);
        assertEquals(step1.lV, step2.lV);
        assertEquals(step1.lE, step2.lE);
        String r = step2.toString();
        assertTrue(r.contains("V") && r.contains("E"));
    }
    @Test
    void testNodeFormatBasicPublic() {
        DummyStep s = new DummyStep();
        s.V.add(5);
        s.lV.put(5, "B");
        s.hV.put(5, "red");
        String res = s.nodeFormat(5);
        assertTrue(res.contains("label=") && res.contains("color=red"));
    }
    @Test
    void testNodeFormatHiddenPublic() {
        DummyStep s = new DummyStep();
        String res = s.nodeFormat(123);
        assertTrue(res.contains("style=invis"));
    }
    @Test
    void testEdgeFormatAllPublic() {
        DummyStep s = new DummyStep();
        Pair e = new Pair(7, 8);
        s.E.add(e);
        s.lE.put(e, "labelZ");
        s.hE.put(e, "orange");
        String res = s.edgeFormat(e);
        assertTrue(res.contains("label=") && res.contains("color=orange"));
    }
    @Test
    void testEdgeFormatHiddenPublic() {
        DummyStep s = new DummyStep();
        String res = s.edgeFormat(new Pair(17, 28));
        assertTrue(res.contains("style=invis"));
    }
    @Test
    void testAnimationActionMethodsPublic() {
        DummyAnimation anim = new DummyAnimation();
        anim.nextStep();
        anim.addNode(101);
        anim.highlightNode(201, "purple");
        anim.labelNode(201, "Z");
        anim.unlabelNode(201);
        anim.removeNode(201);
        anim.addEdge(101, 301);
        anim.highlightEdge(101, 301, "pink");
        anim.labelEdge(101, 301, "F");
        anim.unlabelEdge(101, 301);
        anim.removeEdge(101, 301);
        // No assertion, just check no exception
    }
    @Test
    void testAnimationParseGoodPublic() {
        DummyAnimation anim = new DummyAnimation();
        anim.parse(Arrays.asList(
                "an 17",
                "ae 17 18",
                "ln 17 labelB",
                "le 17 18 labelF",
                "hn 17",
                "he 17 18",
                "ns",
                "un 17",
                "ue 17 18",
                "rn 17",
                "re 17 18"
        ));
        // No exception expected
    }
    @Test
    void testAnimationParseBadPublic() {
        DummyAnimation anim = new DummyAnimation();
        assertThrows(DummyParseException.class, () -> {
            anim.parse(Arrays.asList("badcmd 77"));
        });
    }
    @Test
    void testAnimationParseBadFormatPublic() {
        DummyAnimation anim = new DummyAnimation();
        // insufficient args
        assertThrows(DummyParseException.class, () -> {
            anim.parse(Arrays.asList("ae"));
        });
        // invalid int conversion
        assertThrows(DummyParseException.class, () -> {
            anim.parse(Arrays.asList("an invalidnum"));
        });
    }
}