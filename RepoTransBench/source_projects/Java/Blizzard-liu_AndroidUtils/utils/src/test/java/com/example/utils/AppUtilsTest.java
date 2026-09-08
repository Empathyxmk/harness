package com.example.utils;

import android.content.Context;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;

import org.junit.Test;
import org.mockito.Mockito;
import static org.junit.Assert.*;

public class AppUtilsTest {

    @Test
    public void testGetVerCode_normal() throws Exception {
        Context context = Mockito.mock(Context.class);
        PackageManager pm = Mockito.mock(PackageManager.class);
        PackageInfo info = new PackageInfo();
        info.versionCode = 123;
        Mockito.when(context.getPackageName()).thenReturn("pkg");
        Mockito.when(context.getPackageManager()).thenReturn(pm);
        Mockito.when(pm.getPackageInfo("pkg", 0)).thenReturn(info);
        assertEquals(123, AppUtils.getVerCode(context));
    }

    @Test
    public void testGetVerCode_notFound() throws Exception {
        Context context = Mockito.mock(Context.class);
        PackageManager pm = Mockito.mock(PackageManager.class);
        Mockito.when(context.getPackageName()).thenReturn("pkg");
        Mockito.when(context.getPackageManager()).thenReturn(pm);
        Mockito.when(pm.getPackageInfo(Mockito.anyString(), Mockito.anyInt()))
                .thenThrow(new PackageManager.NameNotFoundException());
        assertEquals(-1, AppUtils.getVerCode(context));
    }

    @Test
    public void testGetVerName_normal() throws Exception {
        Context context = Mockito.mock(Context.class);
        PackageManager pm = Mockito.mock(PackageManager.class);
        PackageInfo info = new PackageInfo();
        info.versionName = "verX";
        Mockito.when(context.getPackageName()).thenReturn("pkg");
        Mockito.when(context.getPackageManager()).thenReturn(pm);
        Mockito.when(pm.getPackageInfo("pkg", 0)).thenReturn(info);
        assertEquals("verX", AppUtils.getVerName(context));
    }

    @Test
    public void testGetVerName_notFound() throws Exception {
        Context context = Mockito.mock(Context.class);
        PackageManager pm = Mockito.mock(PackageManager.class);
        Mockito.when(context.getPackageName()).thenReturn("pkg");
        Mockito.when(context.getPackageManager()).thenReturn(pm);
        Mockito.when(pm.getPackageInfo(Mockito.anyString(), Mockito.anyInt()))
                .thenThrow(new PackageManager.NameNotFoundException());
        assertEquals("", AppUtils.getVerName(context));
    }
}