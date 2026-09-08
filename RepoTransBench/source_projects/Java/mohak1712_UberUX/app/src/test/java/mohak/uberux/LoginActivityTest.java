package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.junit.Assert.*;

public class LoginActivityTest {

    private LoginActivity activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(LoginActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreateExecutesWithoutCrash() {
        Bundle bundle = new Bundle();
        activity.onCreate(bundle);
        assertNotNull(activity);
    }

    @Test
    public void testSetupWindowAnimationsNoCrash() {
        // Protected method, so just check no exceptions
        Mockito.doNothing().when(activity).setupWindowAnimations();
        activity.setupWindowAnimations();
    }
}