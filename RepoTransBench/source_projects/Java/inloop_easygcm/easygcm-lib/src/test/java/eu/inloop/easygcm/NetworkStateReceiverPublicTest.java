package eu.inloop.easygcm;

import android.content.Context;
import android.content.Intent;
import android.support.v4.content.WakefulBroadcastReceiver;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

public class NetworkStateReceiverPublicTest {

    Context mockContext;
    Intent mockIntent;

    @Before
    public void setup() {
        mockContext = mock(Context.class);
        mockIntent = mock(Intent.class);
    }

    @Test
    public void testReceive_registersWhenAllowed_public() {
        try {
            GcmUtilsStubberPublic.setCheckCanAndShouldRegisterResult(true);

            Intent regIntent = new Intent(mockContext, Object.class); // Use different intent to change test data
            GcmRegistrationServiceStubberPublic.setCreateGcmRegistrationIntentResult(regIntent);

            NetworkStateReceiver receiver = new NetworkStateReceiver();
            WakefulBroadcastReceiver spyReceiver = Mockito.spy(receiver);

            doNothing().when(spyReceiver).startWakefulService(any(Context.class), any(Intent.class));

            spyReceiver.onReceive(mockContext, mockIntent);

            verify(spyReceiver).startWakefulService(eq(mockContext), eq(regIntent));
        } finally {
            GcmUtilsStubberPublic.reset();
            GcmRegistrationServiceStubberPublic.reset();
        }
    }

    @Test
    public void testReceive_doesNothingIfNotAllowed_public() {
        try {
            GcmUtilsStubberPublic.setCheckCanAndShouldRegisterResult(false);
            NetworkStateReceiver receiver = new NetworkStateReceiver();
            WakefulBroadcastReceiver spyReceiver = Mockito.spy(receiver);
            spyReceiver.onReceive(mockContext, mockIntent);
            verify(spyReceiver, never()).startWakefulService(any(Context.class), any(Intent.class));
        } finally {
            GcmUtilsStubberPublic.reset();
            GcmRegistrationServiceStubberPublic.reset();
        }
    }
}

// --- Static stubbers with public-specific data ---

class GcmUtilsStubberPublic {
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

class GcmRegistrationServiceStubberPublic {
    static Intent forcedIntent = null;

    static void setCreateGcmRegistrationIntentResult(Intent intent) {
        forcedIntent = intent;
    }

    static void reset() {
        forcedIntent = null;
    }
}

// Patch for public test
class GcmUtils {
    static boolean checkCanAndShouldRegister(Context context) {
        if (GcmUtilsStubberPublic.override) return GcmUtilsStubberPublic.forcedResult;
        return false;
    }
}
class GcmRegistrationService {
    static Intent createGcmRegistrationIntent(Context context, boolean hasWakeLock) {
        if (GcmRegistrationServiceStubberPublic.forcedIntent != null)
            return GcmRegistrationServiceStubberPublic.forcedIntent;
        return new Intent();
    }
}