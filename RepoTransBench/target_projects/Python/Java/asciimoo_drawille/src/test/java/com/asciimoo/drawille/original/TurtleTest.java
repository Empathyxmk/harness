package com.asciimoo.drawille.original;

import com.asciimoo.drawille.Turtle;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TurtleTest {

    @Test
    void testPosition() {
        Turtle t = new Turtle();
        assertEquals(0, t.pos_x);
        assertEquals(0, t.pos_y);
        t.move(1, 1);
        assertEquals(1, t.pos_x);
        assertEquals(1, t.pos_y);
    }

    @Test
    void testRotation() {
        Turtle t = new Turtle();
        assertEquals(0, t.rotation);
        t.right(30);
        assertEquals(30, t.rotation);
        t.left(30);
        assertEquals(0, t.rotation);
    }

    @Test
    void testBrush() {
        Turtle t = new Turtle();
        assertFalse(t.get(t.pos_x, t.pos_y));
        t.forward(1);
        assertTrue(t.get(0, 0));
        assertTrue(t.get(t.pos_x, t.pos_y));
        t.up();
        t.move(2, 0);
        assertFalse(t.get(t.pos_x, t.pos_y));
        t.down();
        t.move(3, 0);
        assertTrue(t.get(t.pos_x, t.pos_y));
    }
}