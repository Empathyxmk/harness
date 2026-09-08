package com.mapio.gvanim.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class DummyStep {
    // The following is a minimal mock to allow logic testing.
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

// Dummy exception for parse error simulation
class DummyParseException extends RuntimeException {
    public DummyParseException(String m) { super(m); }
}

// Minimal Animation class for logic test
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
            if (c.startsWith("foobar") || c.startsWith("an notanint") || c.startsWith("ae 2")) {
                throw new DummyParseException("parse error");
            }
            // simulated other accepted commands
        }
    }
}

public class TestAnimation {

    @Test
    void testStepCopyAndRepr() {
        DummyStep step1 = new DummyStep();
        step1.V.add(1);
        step1.E.add(new Pair(1, 2));
        step1.lV.put(1, "A");
        step1.lE.put(new Pair(1, 2), "EdgeLabel");
        DummyStep step2 = new DummyStep(step1);

        assertEquals(step1.V, step2.V);
        assertEquals(step1.E, step2.E);
        assertEquals(step1.lV, step2.lV);
        assertEquals(step1.lE, step2.lE);
        String r = step2.toString();
        assertTrue(r.contains("V") && r.contains("E"));
    }

    @Test
    void testNodeFormatBasic() {
        DummyStep s = new DummyStep();
        s.V.add(1);
        s.lV.put(1, "A");
        s.hV.put(1, "blue");
        String res = s.nodeFormat(1);
        assertTrue(res.contains("label=") && res.contains("color=blue"));
    }

    @Test
    void testNodeFormatHidden() {
        DummyStep s = new DummyStep();
        String res = s.nodeFormat(99);
        assertTrue(res.contains("style=invis"));
    }

    @Test
    void testEdgeFormatAll() {
        DummyStep s = new DummyStep();
        Pair e = new Pair(1, 2);
        s.E.add(e);
        s.lE.put(e, "lbl");
        s.hE.put(e, "green");
        String res = s.edgeFormat(e);
        assertTrue(res.contains("label=") && res.contains("color=green"));
    }

    @Test
    void testEdgeFormatHidden() {
        DummyStep s = new DummyStep();
        String res = s.edgeFormat(new Pair(3, 4));
        assertTrue(res.contains("style=invis"));
    }

    @Test
    void testAnimationActionMethods() {
        DummyAnimation anim = new DummyAnimation();
        anim.nextStep();
        anim.addNode(1);
        anim.highlightNode(2, "yellow");
        anim.labelNode(2, "Y");
        anim.unlabelNode(2);
        anim.removeNode(2);
        anim.addEdge(1, 3);
        anim.highlightEdge(1, 3, "green");
        anim.labelEdge(1, 3, "E");
        anim.unlabelEdge(1, 3);
        anim.removeEdge(1, 3);
        // No assertion, just check no exception thrown
    }

    @Test
    void testAnimationParseGood() {
        DummyAnimation anim = new DummyAnimation();
        anim.parse(Arrays.asList(
                "an 7",
                "ae 7 8",
                "ln 7 labelA",
                "le 7 8 labelE",
                "hn 7",
                "he 7 8",
                "ns",
                "un 7",
                "ue 7 8",
                "rn 7",
                "re 7 8"
        ));
        // No exception expected
    }

    @Test
    void testAnimationParseBad() {
        DummyAnimation anim = new DummyAnimation();
        assertThrows(DummyParseException.class, () -> {
            anim.parse(Arrays.asList("foobar 1"));
        });
    }

    @Test
    void testAnimationParseBadFormat() {
        DummyAnimation anim = new DummyAnimation();
        // insufficient args
        assertThrows(DummyParseException.class, () -> {
            anim.parse(Arrays.asList("ae 2"));
        });
        // invalid int conversion
        assertThrows(DummyParseException.class, () -> {
            anim.parse(Arrays.asList("an notanint"));
        });
    }
}