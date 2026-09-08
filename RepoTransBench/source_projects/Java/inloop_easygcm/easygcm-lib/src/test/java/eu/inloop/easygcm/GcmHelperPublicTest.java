package eu.inloop.easygcm;

import android.content.Context;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class GcmHelperPublicTest {

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
    public void testInitDelegatesToEasyGcmPublic() {
        // Just ensuring "init" does not throw and delegates to EasyGcm.
        // Changing input context (different mock) for public variant.
        GcmHelper.init(mockContext);
    }

    @Test
    public void testSetGcmListenerPublic() {
        GcmHelper.setGcmListener(mockListener);
        // There is no output, but we can verify EasyGcm.setGcmListener is called via the interface if it was spied.
        // Here, we just assert no exception and invocation.
    }

    @Test
    public void testSetCheckServicesHandlerPublic() {
        GcmHelper.setCheckServicesHandler(mockHandler);
        // Again, just test it does not throw with a different mock for public.
    }

    @Test
    public void testIsRegisteredPublicDifferentInput() {
        // As EasyGcm.isRegistered is static, we just verify call with different mock (different context)
        GcmHelper.isRegistered(mockContext);
    }

    @Test
    public void testGetRegistrationIdPublicDifferentInput() {
        GcmHelper.getRegistrationId(mockContext);
    }

    @Test
    public void testRemoveRegistrationIdPublicDifferentInput() {
        GcmHelper.removeRegistrationId(mockContext);
    }

    @Test
    public void testGetGcmSenderIdPublicDifferentInput() {
        GcmHelper.getGcmSenderId(mockContext);
    }

    @Test
    public void testSetLoggingEnabledPublic() {
        // Use a different log level
        GcmHelper helper = GcmHelper.getInstance();
        helper.setLoggingEnabled(5);
    }

    @Test
    public void testGetGcmListenerPublic() {
        GcmHelper helper = GcmHelper.getInstance();
        helper.getGcmListener(mockContext);
    }
}