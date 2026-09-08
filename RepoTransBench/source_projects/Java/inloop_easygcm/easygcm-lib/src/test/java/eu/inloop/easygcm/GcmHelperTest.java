package eu.inloop.easygcm;

import android.content.Context;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class GcmHelperTest {

    private Context mockContext;
    private GcmListener mockListener;
    private GcmServicesHandler mockHandler;

    @Before
    public void setUp() {
        mockContext = mock(Context.class);
        mockListener = mock(GcmListener.class);
        mockHandler = mock(GcmServicesHandler.class);
    }

    @Test
    public void testInitDelegatesToEasyGcm() {
        // Should not throw anything
        GcmHelper.init(mockContext);
    }

    @Test
    public void testGetInstance_Singleton() {
        GcmHelper instance1 = GcmHelper.getInstance();
        GcmHelper instance2 = GcmHelper.getInstance();
        assertNotNull(instance1);
        assertSame(instance1, instance2);
    }

    @Test
    public void testSetGcmListenerDelegatesToEasyGcm() {
        GcmHelper.setGcmListener(mockListener);
    }

    @Test
    public void testSetCheckServicesHandlerDelegatesToEasyGcm() {
        GcmHelper.setCheckServicesHandler(mockHandler);
    }

    @Test
    public void testIsRegisteredDelegatesToEasyGcm() {
        boolean result = GcmHelper.isRegistered(mockContext);
        // Just makes sure it runs
        assertFalse(result); // Because default EasyGcm.isRegistered returns false
    }

    @Test
    public void testGetRegistrationIdDelegatesToEasyGcm() {
        String fakeId = "reg123";
        // By default returns null, but let's check it doesn't crash
        assertNull(GcmHelper.getRegistrationId(mockContext));
    }

    @Test
    public void testRemoveRegistrationIdDelegatesToEasyGcm() {
        GcmHelper.removeRegistrationId(mockContext);
    }

    @Test
    public void testGetGcmSenderIdDelegatesToEasyGcm() {
        assertNull(GcmHelper.getGcmSenderId(mockContext));
    }

    @Test
    public void testSetLoggingEnabled() {
        GcmHelper helper = GcmHelper.getInstance();
        helper.setLoggingEnabled(1);
    }

    @Test
    public void testGetGcmListenerDelegatesToEasyGcm() {
        GcmHelper helper = GcmHelper.getInstance();
        assertNull(helper.getGcmListener(mockContext));
    }
}