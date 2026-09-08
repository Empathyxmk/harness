package eu.inloop.easygcm;

import android.content.Context;
import android.content.Intent;
import android.support.v4.content.WakefulBroadcastReceiver;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

public class NetworkStateReceiverTest {

    Context mockContext;
    Intent mockIntent;

    @Before
    public void setup() {
        mockContext = mock(Context.class);
        mockIntent = mock(Intent.class);
    }

    @Test
    public void testReceive_registersWhenAllowed() {
        // Patch static methods with Mockito's spy where possible, else use reflection for workaround in integration
        try {
            // Patch GcmUtils.checkCanAndShouldRegister
            GcmUtilsStubber.setCheckCanAndShouldRegisterResult(true);
            // Patch GcmRegistrationService.createGcmRegistrationIntent
            Intent regIntent = new Intent();
            GcmRegistrationServiceStubber.setCreateGcmRegistrationIntentResult(regIntent);

            NetworkStateReceiver receiver = new NetworkStateReceiver();
            WakefulBroadcastReceiver spyReceiver = Mockito.spy(receiver);

            doNothing().when(spyReceiver).startWakefulService(any(Context.class), any(Intent.class));

            spyReceiver.onReceive(mockContext, mockIntent);

            verify(spyReceiver).startWakefulService(mockContext, regIntent);
        } finally {
            GcmUtilsStubber.reset();
            GcmRegistrationServiceStubber.reset();
        }
    }

    @Test
    public void testReceive_doesNothingIfNotAllowed() {
        try {
            GcmUtilsStubber.setCheckCanAndShouldRegisterResult(false);
            NetworkStateReceiver receiver = new NetworkStateReceiver();
            WakefulBroadcastReceiver spyReceiver = Mockito.spy(receiver);
            spyReceiver.onReceive(mockContext, mockIntent);
            verify(spyReceiver, never()).startWakefulService(any(Context.class), any(Intent.class));
        } finally {
            GcmUtilsStubber.reset();
            GcmRegistrationServiceStubber.reset();
        }
    }
}

// --- Static stubbers for test injection ---

class GcmUtilsStubber {
    static boolean forcedResult;
    static boolean override = false;

    static void setCheckCanAndShouldRegisterResult(boolean result) {
        forcedResult = result;
        override = true;
    }

    static void reset() {
        forcedResult = false;
        override = false;
    }
}

class GcmRegistrationServiceStubber {
    static Intent forcedIntent = null;

    static void setCreateGcmRegistrationIntentResult(Intent intent) {
        forcedIntent = intent;
    }

    static void reset() {
        forcedIntent = null;
    }
}

// === Patch the classes used in NetworkStateReceiver for the above static stub ===

class GcmUtils {
    static boolean checkCanAndShouldRegister(Context context) {
        if (GcmUtilsStubber.override) return GcmUtilsStubber.forcedResult;
        return false;
    }
}
class GcmRegistrationService {
    static Intent createGcmRegistrationIntent(Context context, boolean hasWakeLock) {
        if (GcmRegistrationServiceStubber.forcedIntent != null)
            return GcmRegistrationServiceStubber.forcedIntent;
        return new Intent();
    }
}