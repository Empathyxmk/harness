package com.github.fafaldo.fabtoolbar.util;

import org.junit.Test;

import static org.junit.Assert.*;

public class ExpandAnimationUtilsPublicTest {
    @Test
    public void testGetWidthAfterCollapse_withOtherParams() {
        int initialWidth = 100;
        int deltaWidth = 25;
        int expected = 75;
        int result = ExpandAnimationUtils.getWidthAfterCollapse(initialWidth, deltaWidth);
        assertEquals(expected, result);
    }

    @Test
    public void testGetWidthAfterExpand_withOtherParams() {
        int initialWidth = 150;
        int deltaWidth = 45;
        int expected = 195;
        int result = ExpandAnimationUtils.getWidthAfterExpand(initialWidth, deltaWidth);
        assertEquals(expected, result);
    }
}