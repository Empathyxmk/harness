package eu.inloop.easygcm;

import android.os.Bundle;

import com.google.android.gms.gcm.GcmListenerService;

import org.junit.Test;

import static org.mockito.Mockito.*;

public class EasyGcmListenerServiceTest {

    @Test
    public void testOnMessageReceived_delegatesToEasyGcm() {
        String from = "sender";
        Bundle data = new Bundle();
        data.putString("key", "value");

        // Patch EasyGcm.getInstance().getGcmListener().onMessage()
        EasyGcmStubber.setGcmListenerSpy();

        EasyGcmListenerService service = new EasyGcmListenerService();
        service.onMessageReceived(from, data);

        assertTrue(EasyGcmStubber.calledOnMessage);
        EasyGcmStubber.reset();
    }
}

// --- Stubber classes to patch EasyGcm static/singleton for test isolation ---

class EasyGcmStubber {
    static boolean calledOnMessage = false;

    static void setGcmListenerSpy() {
        EasyGcm.getInstance().setGcmListener(new GcmListener() {
            @Override
            public void onMessage(String from, Bundle data) {
                calledOnMessage = true;
            }
            // Add any other necessary stub methods if required
        });
    }
    static void reset() {
        calledOnMessage = false;
    }
}

// You could create empty EasyGcm, GcmListener stubs/interfaces for testing if not present