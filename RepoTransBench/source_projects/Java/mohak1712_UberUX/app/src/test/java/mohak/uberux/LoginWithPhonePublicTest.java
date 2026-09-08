package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.junit.Assert.*;

public class LoginWithPhonePublicTest {
    private LoginWithPhone activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(LoginWithPhone.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreate_noCrash_public() {
        // Different data for test
        Bundle bundle = new Bundle();
        bundle.putInt("public_test_number", 42);
        activity.onCreate(bundle);
        assertNotNull(activity);
    }

    @Test
    public void testSetupWindowAnimations_noCrash_public() {
        Mockito.doNothing().when(activity).setupWindowAnimations();
        activity.setupWindowAnimations();
    }
}