package eu.inloop.easygcm;

import android.content.Context;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class ConnectionUtilsPublicTest {

    private Context mockContext;
    private PackageManager mockPackageManager;
    private ConnectivityManager mockConnectivityManager;
    private NetworkInfo mockNetworkInfo;

    @Before
    public void setUp() {
        mockContext = mock(Context.class);
        mockPackageManager = mock(PackageManager.class);
        mockConnectivityManager = mock(ConnectivityManager.class);
        mockNetworkInfo = mock(NetworkInfo.class);

        when(mockContext.getPackageManager()).thenReturn(mockPackageManager);
        // Use a different package name for public test to ensure input is different.
        when(mockContext.getPackageName()).thenReturn("eu.inloop.easygcm.publictest");
    }

    @Test
    public void testHasAccessNetworkStatePermission_granted_different() {
        when(mockPackageManager.checkPermission(eq("android.permission.ACCESS_NETWORK_STATE"), eq("eu.inloop.easygcm.publictest")))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        assertTrue(ConnectionUtils.hasAccessNetworkStatePermission(mockContext));
    }

    @Test
    public void testHasAccessNetworkStatePermission_denied_different() {
        when(mockPackageManager.checkPermission(eq("android.permission.ACCESS_NETWORK_STATE"), eq("eu.inloop.easygcm.publictest")))
                .thenReturn(PackageManager.PERMISSION_DENIED);
        assertFalse(ConnectionUtils.hasAccessNetworkStatePermission(mockContext));
    }

    @Test
    public void testIsOnline_withPermissionAndConnected_different() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE))
                .thenReturn(mockConnectivityManager);
        when(mockConnectivityManager.getActiveNetworkInfo()).thenReturn(mockNetworkInfo);
        // Flip logic: previously true, now check with false first.
        when(mockNetworkInfo.isConnected()).thenReturn(true);

        assertTrue(ConnectionUtils.isOnline(mockContext));
    }

    @Test
    public void testIsOnline_withPermissionAndNotConnected_different() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE))
                .thenReturn(mockConnectivityManager);
        when(mockConnectivityManager.getActiveNetworkInfo()).thenReturn(mockNetworkInfo);
        // Flip to opposite to change test data
        when(mockNetworkInfo.isConnected()).thenReturn(false);

        assertFalse(ConnectionUtils.isOnline(mockContext));
    }

    @Test
    public void testIsOnline_withPermissionAndNoNetworkInfo_different() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE))
                .thenReturn(mockConnectivityManager);
        // Different test: return null but permission is granted.
        when(mockConnectivityManager.getActiveNetworkInfo()).thenReturn(null);

        assertFalse(ConnectionUtils.isOnline(mockContext));
    }

    @Test
    public void testIsOnline_withoutPermission_different() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_DENIED);
        // This should exercise the "hope for best" branch as in the original.
        assertTrue(ConnectionUtils.isOnline(mockContext)); 
    }
}