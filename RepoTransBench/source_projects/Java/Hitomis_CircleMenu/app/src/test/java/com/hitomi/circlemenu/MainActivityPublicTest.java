package com.hitomi.circlemenu;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;

import com.hitomi.cmlibrary.CircleMenu;

import org.junit.Before;
import org.junit.Test;

import static org.mockito.Mockito.*;

/**
 * Public test for MainActivity, using different logic invocation and additional scenario compared to the main test.
 */
public class MainActivityPublicTest {
    private MainActivity mainActivity;
    private CircleMenu mockCircleMenu;

    @Before
    public void setUp() {
        mainActivity = new MainActivity();
        mockCircleMenu = mock(CircleMenu.class);

        try {
            java.lang.reflect.Field field = MainActivity.class.getDeclaredField("circleMenu");
            field.setAccessible(true);
            field.set(mainActivity, mockCircleMenu);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    public void test_onMenuOpened_callsOpenMenu_twice() {
        Menu mockMenu = mock(Menu.class);
        when(mockCircleMenu.openMenu()).thenReturn(null);

        // Call the menu-opened logic twice in the public test
        mainActivity.onMenuOpened(2, mockMenu);
        mainActivity.onMenuOpened(3, mockMenu);

        verify(mockCircleMenu, times(2)).openMenu();
    }

    @Test
    public void test_onBackPressed_callsCircleMenuCloseMenu_multipleTimes() {
        doNothing().when(mockCircleMenu).closeMenu();

        mainActivity.onBackPressed();
        mainActivity.onBackPressed();

        verify(mockCircleMenu, times(2)).closeMenu();
    }
}