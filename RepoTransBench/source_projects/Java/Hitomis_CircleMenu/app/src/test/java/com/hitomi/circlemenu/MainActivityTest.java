package com.hitomi.circlemenu;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;

import com.hitomi.cmlibrary.CircleMenu;
import com.hitomi.cmlibrary.OnMenuSelectedListener;
import com.hitomi.cmlibrary.OnMenuStatusChangeListener;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class MainActivityTest {

    private MainActivity mainActivity;
    private CircleMenu mockCircleMenu;

    @Before
    public void setUp() {
        mainActivity = new MainActivity();
        mockCircleMenu = mock(CircleMenu.class);
        // Use reflection to inject the mock CircleMenu since MainActivity references it directly
        try {
            java.lang.reflect.Field field = MainActivity.class.getDeclaredField("circleMenu");
            field.setAccessible(true);
            field.set(mainActivity, mockCircleMenu);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    public void test_onMenuOpened_callsCircleMenuOpenMenu() {
        Menu mockMenu = mock(Menu.class);
        when(mockCircleMenu.openMenu()).thenReturn(null);

        // super.onMenuOpened returns false by default
        boolean result = mainActivity.onMenuOpened(1, mockMenu);

        verify(mockCircleMenu, times(1)).openMenu();
    }

    @Test
    public void test_onBackPressed_callsCircleMenuCloseMenu() {
        doNothing().when(mockCircleMenu).closeMenu();

        mainActivity.onBackPressed();

        verify(mockCircleMenu, times(1)).closeMenu();
    }

}