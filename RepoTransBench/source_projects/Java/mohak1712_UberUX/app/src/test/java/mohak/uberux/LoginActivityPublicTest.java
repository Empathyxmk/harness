package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.junit.Assert.*;

public class LoginActivityPublicTest {

    private LoginActivity activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(LoginActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreateExecutesWithoutCrash_public() {
        // New bundle data
        Bundle bundle = new Bundle();
        bundle.putString("public_test_key", "public_test_value");
        activity.onCreate(bundle);
        assertNotNull(activity);
    }

    @Test
    public void testSetupWindowAnimationsNoCrash_public() {
        Mockito.doNothing().when(activity).setupWindowAnimations();
        activity.setupWindowAnimations();
    }
}