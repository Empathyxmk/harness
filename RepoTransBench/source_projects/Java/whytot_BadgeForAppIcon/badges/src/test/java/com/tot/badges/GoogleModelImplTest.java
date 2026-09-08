package com.tot.badges;

import android.app.Application;
import android.app.Notification;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.os.Build;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import java.lang.reflect.Field;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class GoogleModelImplTest {

    private GoogleModelImpl googleModel;

    @Mock
    Application mockApplication;
    @Mock
    Notification mockNotification;
    @Mock
    PackageManager mockPackageManager;
    @Mock
    Utils mockUtils;

    // Use a custom method to set SDK_INT for testing purposes
    private void setSdkInt(int value) {
        SdkVersionMocker.setSdkVersion(value);
    }

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        googleModel = new GoogleModelImpl();

        // Mock Utils.getInstance() to return our mockUtils
        // This is necessary because GoogleModelImpl calls Utils.getInstance()
        try {
            Field instanceField = Utils.class.getDeclaredField("instance");
            instanceField.setAccessible(true);
            instanceField.set(null, mockUtils);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to mock Utils instance", e);
        }

        // Default mock for Utils methods that GoogleModelImpl uses
        when(mockUtils.getLaunchIntentForPackage(any(Application.class))).thenReturn("com.example.package.MainActivity");
        when(mockUtils.canResolveBroadcast(any(Context.class), any(Intent.class))).thenReturn(true);
        when(mockApplication.getPackageName()).thenReturn("com.example.package");
        when(mockApplication.getPackageManager()).thenReturn(mockPackageManager); // Required for canResolveBroadcast in Utils if not mocked directly
    }

    @After
    public void tearDown() {
        SdkVersionMocker.resetSdkVersion(); // Reset SDK_INT after each test
        // Reset Utils instance to null to avoid interference with other tests that might use it
        try {
            Field instanceField = Utils.class.getDeclaredField("instance");
            instanceField.setAccessible(true);
            instanceField.set(null, null);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to reset Utils instance", e);
        }
    }

    @Test
    public void testSetIconBadgeNum_sdkBelowO() {
        setSdkInt(Build.VERSION_CODES.N_MR1); // SDK_INT = 25 (below O)

        try {
            googleModel.setIconBadgeNum(mockApplication, mockNotification, 5);
            fail("Expected an Exception for SDK below O");
        } catch (Exception e) {
            assertEquals("google not support before API O", e.getMessage());
            verify(mockApplication, never()).sendBroadcast(any(Intent.class));
        }
    }

    @Test
    public void testSetIconBadgeNum_sdkAtOrAboveO() throws Exception {
        setSdkInt(Build.VERSION_CODES.O); // SDK_INT = 26 (O)
        int testCount = 7;

        googleModel.setIconBadgeNum(mockApplication, mockNotification, testCount);

        ArgumentCaptor<Intent> intentCaptor = ArgumentCaptor.forClass(Intent.class);
        verify(mockApplication, times(1)).sendBroadcast(intentCaptor.capture());

        Intent capturedIntent = intentCaptor.getValue();
        assertEquals("android.intent.action.BADGE_COUNT_UPDATE", capturedIntent.getAction());
        assertEquals(testCount, capturedIntent.getIntExtra("badge_count", 0));
        assertEquals("com.example.package", capturedIntent.getStringExtra("badge_count_package_name"));
        assertEquals("com.example.package.MainActivity", capturedIntent.getStringExtra("badge_count_class_name"));
    }
}