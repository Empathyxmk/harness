package google.architecture.coremodel.util;

import android.arch.lifecycle.LiveData;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class NetUtilsTest {

    Context mockContext;
    ConnectivityManager mockConnectivityManager;
    NetworkInfo mockWifiInfo;
    NetworkInfo mockEthInfo;

    @Before
    public void setup() {
        mockContext = mock(Context.class);
        mockConnectivityManager = mock(ConnectivityManager.class);
        when(mockContext.getSystemService(Context.CONNECTIVITY_SERVICE)).thenReturn(mockConnectivityManager);

        mockWifiInfo = mock(NetworkInfo.class);
        mockEthInfo = mock(NetworkInfo.class);
    }

    @Test
    public void testGetNetConnStatus_nullContext() {
        int status = NetUtils.getNetConnStatus(null);
        assertEquals(NetUtils.DISCONNECTED, status);
    }

    @Test
    public void testGetNetConnStatus_wifiConnected() {
        when(mockConnectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI)).thenReturn(mockWifiInfo);
        when(mockWifiInfo.isAvailable()).thenReturn(true);
        when(mockWifiInfo.isConnected()).thenReturn(true);

        int status = NetUtils.getNetConnStatus(mockContext);
        assertEquals(NetUtils.WIFI_CONNECTED, status);
    }

    @Test
    public void testGetNetConnStatus_ethernetConnected() {
        when(mockConnectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI)).thenReturn(mockWifiInfo);
        when(mockWifiInfo.isAvailable()).thenReturn(false);

        when(mockConnectivityManager.getNetworkInfo(ConnectivityManager.TYPE_ETHERNET)).thenReturn(mockEthInfo);
        when(mockEthInfo.isAvailable()).thenReturn(true);
        when(mockEthInfo.isConnected()).thenReturn(true);

        int status = NetUtils.getNetConnStatus(mockContext);
        assertEquals(NetUtils.ETHERNET_CONNECTED, status);
    }

    @Test
    public void testGetNetConnStatus_none() {
        when(mockConnectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI)).thenReturn(null);
        when(mockConnectivityManager.getNetworkInfo(ConnectivityManager.TYPE_ETHERNET)).thenReturn(null);
        int status = NetUtils.getNetConnStatus(mockContext);
        assertEquals(NetUtils.DISCONNECTED, status);
    }

    @Test
    public void testIsNetConnected_nullContext() {
        assertFalse(NetUtils.isNetConnected(null));
    }

    @Test
    public void testIsNetConnected_connected() {
        NetworkInfo info = mock(NetworkInfo.class);
        NetworkInfo[] arr = new NetworkInfo[]{info};
        when(info.isConnected()).thenReturn(true);
        when(info.getState()).thenReturn(NetworkInfo.State.CONNECTED);

        when(mockConnectivityManager.getAllNetworkInfo()).thenReturn(arr);
        boolean res = NetUtils.isNetConnected(mockContext);
        assertTrue(res);
    }

    @Test
    public void testIsNetConnected_none() {
        when(mockConnectivityManager.getAllNetworkInfo()).thenReturn(null);
        boolean res = NetUtils.isNetConnected(mockContext);
        assertFalse(res);
    }

    @Test
    public void testIsNetConnected_notConnected() {
        NetworkInfo info = mock(NetworkInfo.class);
        NetworkInfo[] arr = new NetworkInfo[]{info};
        when(info.isConnected()).thenReturn(false);

        when(mockConnectivityManager.getAllNetworkInfo()).thenReturn(arr);
        boolean res = NetUtils.isNetConnected(mockContext);
        assertFalse(res);
    }

    @Test
    public void testNetConnected_nullContext() {
        LiveData<Boolean> live = NetUtils.netConnected(null);
        assertNotNull(live);
        assertEquals(false, live.getValue());
    }
}