package com.tot.badges;

import android.app.Application;
import android.app.Notification;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.lang.reflect.Field;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class GoogleModelImplPublicTest {

    private GoogleModelImpl googleModel;

    @Mock
    Application mockApplication;
    @Mock
    Notification mockNotification;
    @Mock
    PackageManager mockPackageManager;
    @Mock
    Utils mockUtils;

    private void setSdkInt(int value) {
        SdkVersionMocker.setSdkVersion(value);
    }

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        googleModel = new GoogleModelImpl();

        try {
            Field instanceField = Utils.class.getDeclaredField("instance");
            instanceField.setAccessible(true);
            instanceField.set(null, mockUtils);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to mock Utils instance", e);
        }

        when(mockUtils.getLaunchIntentForPackage(any(Application.class))).thenReturn("sample.another.MainAct");
        when(mockUtils.canResolveBroadcast(any(android.content.Context.class), any(Intent.class))).thenReturn(true);
        when(mockApplication.getPackageName()).thenReturn("sample.another");
        when(mockApplication.getPackageManager()).thenReturn(mockPackageManager);
    }

    @After
    public void tearDown() {
        SdkVersionMocker.resetSdkVersion();
        try {
            Field instanceField = Utils.class.getDeclaredField("instance");
            instanceField.setAccessible(true);
            instanceField.set(null, null);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to reset Utils instance", e);
        }
    }

    @Test
    public void testSetIconBadgeNum_sdkBelowO_public() {
        setSdkInt(Build.VERSION_CODES.N); // SDK_INT = 24 (below O)

        try {
            googleModel.setIconBadgeNum(mockApplication, mockNotification, 15);
            fail("Expected an Exception for SDK below O");
        } catch (Exception e) {
            assertEquals("google not support before API O", e.getMessage());
            verify(mockApplication, never()).sendBroadcast(any(Intent.class));
        }
    }

    @Test
    public void testSetIconBadgeNum_sdkAtOrAboveO_public() throws Exception {
        setSdkInt(Build.VERSION_CODES.O_MR1); // SDK_INT = 27
        int testCount = 21;

        googleModel.setIconBadgeNum(mockApplication, mockNotification, testCount);

        ArgumentCaptor<Intent> intentCaptor = ArgumentCaptor.forClass(Intent.class);
        verify(mockApplication, times(1)).sendBroadcast(intentCaptor.capture());

        Intent capturedIntent = intentCaptor.getValue();
        assertEquals("android.intent.action.BADGE_COUNT_UPDATE", capturedIntent.getAction());
        assertEquals(testCount, capturedIntent.getIntExtra("badge_count", 0));
        assertEquals("sample.another", capturedIntent.getStringExtra("badge_count_package_name"));
        assertEquals("sample.another.MainAct", capturedIntent.getStringExtra("badge_count_class_name"));
    }
}