package com.example.publictest;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.figure.Figure;
import com.example.termplotlib.figure.Axes;

import static org.junit.jupiter.api.Assertions.*;

public class TestFigurePublic {
    @Test
    public void testFigureCreationAndAxes() {
        Figure f = new Figure();

        // Add an axis and ensure it's an Axes object
        Axes ax = f.add_subplot(111);
        assertNotNull(ax);
        assertTrue(ax instanceof Axes);

        // Add a second axis
        Axes ax2 = f.add_subplot(112);
        assertNotNull(ax2);
        assertTrue(ax2 instanceof Axes);

        // Check different axes are not the same
        assertNotEquals(ax, ax2);
    }
}