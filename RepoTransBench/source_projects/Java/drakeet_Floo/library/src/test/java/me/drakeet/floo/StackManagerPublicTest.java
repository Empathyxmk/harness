package me.drakeet.floo;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.ArrayList;

public class StackManagerPublicTest {

    private StackManager<String> manager;

    @Before
    public void setUp() {
        manager = new StackManager<>();
    }

    @Test
    public void testPushPop_public() {
        manager.push("alpha");
        manager.push("beta");
        assertEquals("beta", manager.pop());
        assertEquals("alpha", manager.pop());
    }

    @Test
    public void testPopOnEmpty_public() {
        assertNull(manager.pop());
    }
}