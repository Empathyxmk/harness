package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class TargetPublicTest {

    @Test
    public void testCreateAndGetUrl_public() {
        Target target = new Target("foo://bar", "SomeClass");
        assertEquals("foo://bar", target.getUrl());
        assertEquals("SomeClass", target.getTargetClass());
    }

    @Test
    public void testSetUrl_public() {
        Target target = new Target("foo://baz", "OtherClass");
        target.setUrl("foo://changed");
        assertEquals("foo://changed", target.getUrl());
    }
}