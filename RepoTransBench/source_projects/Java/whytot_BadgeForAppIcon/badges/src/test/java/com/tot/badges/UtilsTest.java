package com.tot.badges;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class UtilsTest {

    @Mock
    Context mockContext;
    @Mock
    PackageManager mockPackageManager;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        when(mockContext.getPackageManager()).thenReturn(mockPackageManager);
    }

    @Test
    public void testGetInstance_singleton() {
        Utils instance1 = Utils.getInstance();
        Utils instance2 = Utils.getInstance();
        assertNotNull(instance1);
        assertEquals(instance1, instance2);
    }

    @Test
    public void testCanResolveBroadcast_noReceivers() {
        when(mockPackageManager.queryBroadcastReceivers(any(Intent.class), anyInt())).thenReturn(null);
        assertFalse(Utils.getInstance().canResolveBroadcast(mockContext, new Intent()));

        when(mockPackageManager.queryBroadcastReceivers(any(Intent.class), anyInt())).thenReturn(new ArrayList<ResolveInfo>());
        assertFalse(Utils.getInstance().canResolveBroadcast(mockContext, new Intent()));
    }

    @Test
    public void testCanResolveBroadcast_withReceivers() {
        List<ResolveInfo> receivers = Collections.singletonList(new ResolveInfo());
        when(mockPackageManager.queryBroadcastReceivers(any(Intent.class), anyInt())).thenReturn(receivers);
        assertTrue(Utils.getInstance().canResolveBroadcast(mockContext, new Intent()));
    }

    @Test
    public void testGetLaunchIntentForPackage() {
        Intent mockLaunchIntent = mock(Intent.class);
        ComponentName mockComponentName = mock(ComponentName.class);

        when(mockContext.getPackageName()).thenReturn("com.example.package");
        when(mockPackageManager.getLaunchIntentForPackage(anyString())).thenReturn(mockLaunchIntent);
        when(mockLaunchIntent.getComponent()).thenReturn(mockComponentName);
        when(mockComponentName.getClassName()).thenReturn("com.example.package.MainActivity");

        String className = Utils.getInstance().getLaunchIntentForPackage(mockContext);
        assertEquals("com.example.package.MainActivity", className);
    }

    @Test(expected = NullPointerException.class) // Because getLaunchIntentForPackage can return null, and then .getComponent() would throw NPE
    public void testGetLaunchIntentForPackage_nullLaunchIntent() {
        when(mockContext.getPackageName()).thenReturn("com.example.package");
        when(mockPackageManager.getLaunchIntentForPackage(anyString())).thenReturn(null);

        Utils.getInstance().getLaunchIntentForPackage(mockContext);
    }
}