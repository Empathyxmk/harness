package com.thomasa88.original;

import com.thomasa88.ParamSpec;
import com.thomasa88.Slice;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class TestParser {

    @Test
    void testSplitParam() {
        assertEquals(ParamSpec.fromString("_"), new ParamSpec("_"));
        assertEquals(ParamSpec.fromString("_.version"), new ParamSpec("_", "version", null, null));
        assertEquals(ParamSpec.fromString("_.version:02d"), new ParamSpec("_", "version", null, "02d"));
        assertEquals(ParamSpec.fromString("_.file[1:5]"), new ParamSpec("_", "file", new Slice(1,5), null));
        assertEquals(ParamSpec.fromString("_.file[1:5]:01"), new ParamSpec("_", "file", new Slice(1,5), "01"));
        assertEquals(ParamSpec.fromString("param"), new ParamSpec("param", null, null, null));
        assertEquals(ParamSpec.fromString("param:-<2"), new ParamSpec("param", null, null, "-<2"));
        assertEquals(ParamSpec.fromString("param[1]:-<2"), new ParamSpec("param", null, new Slice(1, 2), "-<2"));
        assertEquals(ParamSpec.fromString("param[-1:]"), new ParamSpec("param", null, new Slice(-1, null), null));
        assertEquals(ParamSpec.fromString("param[:-3]"), new ParamSpec("param", null, new Slice(null, -3), null));
    }

    @Test
    void testSliceParsing() {
        assertEquals(ParamSpec.fromString("p[0]"), new ParamSpec("p", null, new Slice(0, 1), null));
        assertEquals(ParamSpec.fromString("p[:5]"), new ParamSpec("p", null, new Slice(null, 5), null));
        assertEquals(ParamSpec.fromString("p[6:]"), new ParamSpec("p", null, new Slice(6, null), null));
        assertEquals(ParamSpec.fromString("p[5:6]"), new ParamSpec("p", null, new Slice(5, 6), null));
        assertEquals(ParamSpec.fromString("p[:-1]"), new ParamSpec("p", null, new Slice(null, -1), null));
        assertEquals(ParamSpec.fromString("p[1:-2]"), new ParamSpec("p", null, new Slice(1, -2), null));
        assertEquals(ParamSpec.fromString("p[:]"), new ParamSpec("p", null, new Slice(null, null), null));
        assertEquals(ParamSpec.fromString("p[-5:5]"), new ParamSpec("p", null, new Slice(-5,5), null));
        assertEquals(ParamSpec.fromString("p[11:5]"), new ParamSpec("p", null, new Slice(11,5), null));
        assertNull(ParamSpec.fromString("p[]"));
        assertNull(ParamSpec.fromString("p[a]"));
        assertNull(ParamSpec.fromString("p[a:b]"));
        assertNull(ParamSpec.fromString("p[:b]"));
        assertNull(ParamSpec.fromString("p[1:3:2]"));
        assertNull(ParamSpec.fromString("p[::]"));
    }

    @Test
    void testSplitExampleStrings() {
        assertEquals(ParamSpec.fromString("d1:.3f"), new ParamSpec("d1", null, null, ".3f"));
        assertEquals(ParamSpec.fromString("d1.unit"), new ParamSpec("d1", "unit", null, null));
        assertEquals(ParamSpec.fromString("d1:03.0f"), new ParamSpec("d1", null, null, "03.0f"));
        assertEquals(ParamSpec.fromString("width:.0f"), new ParamSpec("width", null, null, ".0f"));
        assertEquals(ParamSpec.fromString("width.expr"), new ParamSpec("width", "expr", null, null));
        assertEquals(ParamSpec.fromString("height.expr"), new ParamSpec("height", "expr", null, null));
        assertEquals(ParamSpec.fromString("_.version"), new ParamSpec("_", "version", null, null));
        assertEquals(ParamSpec.fromString("_.version:03"), new ParamSpec("_", "version", null, "03"));
        assertEquals(ParamSpec.fromString("_.file"), new ParamSpec("_", "file", null, null));
        assertEquals(ParamSpec.fromString("_.component"), new ParamSpec("_", "component", null, null));
        assertEquals(ParamSpec.fromString("_.date"), new ParamSpec("_", "date", null, null));
        assertEquals(ParamSpec.fromString("_.date:%m/%d/%Y"), new ParamSpec("_", "date", null, "%m/%d/%Y"));
        assertEquals(ParamSpec.fromString("_.date:%U"), new ParamSpec("_", "date", null, "%U"));
        assertEquals(ParamSpec.fromString("_.date:%W"), new ParamSpec("_", "date", null, "%W"));
        assertEquals(ParamSpec.fromString("_.date:%H:%M"), new ParamSpec("_", "date", null, "%H:%M"));
    }

    @Test
    void testBadParamString() {
        String[] badStrings = {
            "", ".", ".a", "a.", ".a[10]", ".a:5", ".[]", "a[]", "[]", ":", "a[", "a]", "[1]",
            "a[1", ":5", "a[10:10][]"
        };
        for (String bad : badStrings) {
            assertNull(ParamSpec.fromString(bad), "Input: " + bad);
        }
    }
}