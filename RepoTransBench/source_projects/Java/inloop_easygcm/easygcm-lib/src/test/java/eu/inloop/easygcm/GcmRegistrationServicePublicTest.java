package eu.inloop.easygcm;

import android.content.Context;
import android.content.Intent;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class GcmRegistrationServicePublicTest {

    private Context mockContext;

    @Before
    public void setUp() {
        mockContext = org.mockito.Mockito.mock(Context.class);
    }

    @Test
    public void testCreateGcmRegistrationIntentWithWakeLockPublic() {
        // Using hasWakeLock = false for public test (opposite of typical value in main tests)
        Intent serviceIntent = GcmRegistrationService.createGcmRegistrationIntent(mockContext, false);
        assertNotNull(serviceIntent);
    }

    @Test
    public void testCreateGcmRegistrationIntentWithWakeLockPublicDifferent() {
        // Use hasWakeLock = true to make sure both branches are covered
        Intent serviceIntent = GcmRegistrationService.createGcmRegistrationIntent(mockContext, true);
        assertNotNull(serviceIntent);
    }
}