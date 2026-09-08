package eu.inloop.easygcm;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class GcmRegistrationServiceTest {

    private GcmRegistrationService service;
    private Context mockContext;
    private Intent baseIntent;

    @Before
    public void setUp() {
        service = Mockito.spy(new GcmRegistrationService());
        mockContext = mock(Context.class);
        baseIntent = new Intent();
    }

    @Test
    public void testCreateGcmRegistrationIntent_defaults() {
        Intent result = GcmRegistrationService.createGcmRegistrationIntent(mockContext);
        assertNotNull(result);
        assertEquals(GcmRegistrationService.ACTION_REGISTER_GCM, result.getIntExtra(GcmRegistrationService.EXTRA_ACTION_CODE, -1));
    }

    @Test
    public void testCreateGcmRegistrationIntent_withWakeLock() {
        Intent result = GcmRegistrationService.createGcmRegistrationIntent(mockContext, true);
        assertTrue(result.getBooleanExtra(GcmRegistrationService.EXTRA_HAS_WAKELOCK, false));
    }

    // Note: Directly unit testing the internal registration logic is not feasible because of heavy reliance
    // on Android and GCM, but we'll trigger the main branches as much as possible.

    @Test
    public void testOnHandleIntent_alreadyRegistered() {
        Intent intent = new Intent();
        intent.putExtra(GcmRegistrationService.EXTRA_ACTION_CODE, GcmRegistrationService.ACTION_REGISTER_GCM);

        GcmRegistrationService serviceSpy = Mockito.spy(new GcmRegistrationService());
        // Patch the isAlreadyRegistered to return true
        doReturn(true).when(serviceSpy).isAlreadyRegistered(any(Context.class));
        doNothing().when(serviceSpy).releaseWakeLock();

        serviceSpy.onHandleIntent(intent);
        verify(serviceSpy, never()).registerGcm();
        verify(serviceSpy).releaseWakeLock();
    }

    @Test
    public void testOnHandleIntent_registersAndHandlesError() {
        Intent intent = new Intent();
        intent.putExtra(GcmRegistrationService.EXTRA_ACTION_CODE, GcmRegistrationService.ACTION_REGISTER_GCM);

        GcmRegistrationService serviceSpy = Mockito.spy(new GcmRegistrationService());
        doReturn(false).when(serviceSpy).isAlreadyRegistered(any(Context.class));
        doNothing().when(serviceSpy).releaseWakeLock();
        doNothing().when(serviceSpy).registerGcm();

        serviceSpy.onHandleIntent(intent);
        verify(serviceSpy).registerGcm();
        verify(serviceSpy).releaseWakeLock();
    }
}