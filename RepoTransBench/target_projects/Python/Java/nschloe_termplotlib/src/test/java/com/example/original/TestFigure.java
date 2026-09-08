package com.example.original;

import org.junit.jupiter.api.Test;
import com.example.termplotlib.figure.Figure;

import static org.junit.jupiter.api.Assertions.*;

public class TestFigure {
    @Test
    public void testFigureInit() {
        Figure fig = new Figure();
        assertNotNull(fig);
        assertTrue(fig instanceof Figure);
    }
}