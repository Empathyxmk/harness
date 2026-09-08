package com.hitomi.cmlibrary;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class CircleMenuPublicTest {

    private CircleMenu circleMenu;

    @Before
    public void setUp() {
        // Use a mock Context for pure Java; In real instrumentation, pass actual Context
        circleMenu = new CircleMenu(null, null);
    }

    @Test
    public void test_setMainMenu_differentColor() {
        // Use a different color than in original tests
        circleMenu.setMainMenu(0xFF00FF00, 200, 201);
        assertEquals(0xFF00FF00, circleMenu.getMainMenuColor());
    }

    @Test
    public void test_addSubMenu_differentIcons() {
        circleMenu.addSubMenu(0xFFFF0000, 300);
        assertEquals(1, circleMenu.getSubMenus().size());
        assertEquals(0xFFFF0000, circleMenu.getSubMenus().get(0).getColor());
        assertEquals(300, circleMenu.getSubMenus().get(0).getIconResId());
    }
}