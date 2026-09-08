package eu.inloop.easygcm;

import android.content.Context;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class ConnectionUtilsTest {

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
        when(mockContext.getPackageName()).thenReturn("eu.inloop.easygcm.test");
    }

    @Test
    public void testHasAccessNetworkStatePermission_granted() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        assertTrue(ConnectionUtils.hasAccessNetworkStatePermission(mockContext));
    }

    @Test
    public void testHasAccessNetworkStatePermission_denied() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_DENIED);
        assertFalse(ConnectionUtils.hasAccessNetworkStatePermission(mockContext));
    }

    @Test
    public void testIsOnline_withPermissionAndConnected() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE))
                .thenReturn(mockConnectivityManager);
        when(mockConnectivityManager.getActiveNetworkInfo()).thenReturn(mockNetworkInfo);
        when(mockNetworkInfo.isConnected()).thenReturn(true);

        assertTrue(ConnectionUtils.isOnline(mockContext));
    }

    @Test
    public void testIsOnline_withPermissionAndNotConnected() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE))
                .thenReturn(mockConnectivityManager);
        when(mockConnectivityManager.getActiveNetworkInfo()).thenReturn(mockNetworkInfo);
        when(mockNetworkInfo.isConnected()).thenReturn(false);

        assertFalse(ConnectionUtils.isOnline(mockContext));
    }

    @Test
    public void testIsOnline_withPermissionAndNoNetworkInfo() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_GRANTED);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE))
                .thenReturn(mockConnectivityManager);
        when(mockConnectivityManager.getActiveNetworkInfo()).thenReturn(null);

        assertFalse(ConnectionUtils.isOnline(mockContext));
    }

    @Test
    public void testIsOnline_withoutPermission() {
        when(mockPackageManager.checkPermission(anyString(), anyString()))
                .thenReturn(PackageManager.PERMISSION_DENIED);

        assertTrue(ConnectionUtils.isOnline(mockContext)); // Hope for best branch
    }
}