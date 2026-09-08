package com.github.davidmoten.geo;

import static org.junit.Assert.*;
import org.junit.Test;

public class DirectionPublicTest {

    @Test
    public void testOppositeDifferentOrder() {
        assertEquals(Direction.LEFT, Direction.RIGHT.opposite());
        assertEquals(Direction.RIGHT, Direction.LEFT.opposite());
        assertEquals(Direction.BOTTOM, Direction.TOP.opposite());
        assertEquals(Direction.TOP, Direction.BOTTOM.opposite());
    }
}