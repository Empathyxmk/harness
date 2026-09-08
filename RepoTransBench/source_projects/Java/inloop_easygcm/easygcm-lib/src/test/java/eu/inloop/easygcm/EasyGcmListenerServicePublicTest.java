package eu.inloop.easygcm;

import android.os.Bundle;

import com.google.android.gms.gcm.GcmListenerService;

import org.junit.Test;

import static org.junit.Assert.*;

public class EasyGcmListenerServicePublicTest {

    @Test
    public void testOnMessageReceived_delegatesToEasyGcm_different() {
        String from = "public_sender";
        Bundle data = new Bundle();
        data.putString("another_key", "another_value");

        EasyGcmStubberPublic.setGcmListenerSpy();

        EasyGcmListenerService service = new EasyGcmListenerService();
        service.onMessageReceived(from, data);

        assertTrue(EasyGcmStubberPublic.calledOnMessage);
        EasyGcmStubberPublic.reset();
    }
}

// --- Stubber classes to patch EasyGcm static/singleton for test isolation ---

class EasyGcmStubberPublic {
    static boolean calledOnMessage = false;

    static void setGcmListenerSpy() {
        EasyGcm.getInstance().setGcmListener(new GcmListener() {
            @Override
            public void onMessage(String from, Bundle data) {
                // Check public test data to ensure different route.
                if ("public_sender".equals(from) && "another_value".equals(data.get("another_key"))) {
                    calledOnMessage = true;
                }
            }
        });
    }

    static void reset() {
        calledOnMessage = false;
    }
}