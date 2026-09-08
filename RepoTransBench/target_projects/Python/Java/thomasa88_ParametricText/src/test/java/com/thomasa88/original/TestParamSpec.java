package com.thomasa88.original;

import com.thomasa88.ParamSpec;
import com.thomasa88.Slice;
import com.thomasa88.ParamUtil;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class TestParamSpec {

    @Test
    void testFromStringBasic() {
        ParamSpec ps = ParamSpec.fromString("foo");
        assertEquals(new ParamSpec("foo", null, null, null), ps);
    }

    @Test
    void testFromStringWithMember() {
        ParamSpec ps = ParamSpec.fromString("foo.bar");
        assertEquals(new ParamSpec("foo", "bar", null, null), ps);
    }

    @Test
    void testFromStringWithSlice() {
        ParamSpec ps = ParamSpec.fromString("foo[2]");
        assertEquals(new ParamSpec("foo", null, new Slice(2, 3), null), ps);

        ParamSpec ps2 = ParamSpec.fromString("foo[1:3]");
        assertEquals(new ParamSpec("foo", null, new Slice(1, 3), null), ps2);

        ParamSpec ps3 = ParamSpec.fromString("foo[:4]");
        assertEquals(new ParamSpec("foo", null, new Slice(null, 4), null), ps3);

        ParamSpec ps4 = ParamSpec.fromString("foo[-2:]");
        assertEquals(new ParamSpec("foo", null, new Slice(-2, null), null), ps4);
    }

    @Test
    void testFromStringWithFormat() {
        ParamSpec ps = ParamSpec.fromString("foo:0.2f");
        assertEquals(new ParamSpec("foo", null, null, "0.2f"), ps);

        ps = ParamSpec.fromString("foo.bar[0:2]:spec");
        assertEquals(new ParamSpec("foo", "bar", new Slice(0,2), "spec"), ps);
    }

    @Test
    void testFromStringInvalid() {
        // Invalid string produces null
        assertNull(ParamSpec.fromString("bad["));
    }

    @Test
    void testEq() {
        ParamSpec a = new ParamSpec("foo", "bar", new Slice(1,2), "fmt");
        ParamSpec b = new ParamSpec("foo", "bar", new Slice(1,2), "fmt");
        ParamSpec c = new ParamSpec("foo", "baz", new Slice(1,2), "fmt");
        assertTrue(a.equals(b));
        assertFalse(a.equals(c));
        assertFalse(a.equals(null));
    }

    @Test
    void testNullint() {
        assertEquals(3, ParamUtil.nullint("3"));
        assertNull(ParamUtil.nullint(null));
        assertNull(ParamUtil.nullint(""));
    }
}