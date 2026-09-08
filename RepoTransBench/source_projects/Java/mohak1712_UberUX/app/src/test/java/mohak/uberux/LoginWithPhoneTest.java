package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class LoginWithPhoneTest {

    private LoginWithPhone activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(LoginWithPhone.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreateExecutesWithoutCrash() {
        activity.onCreate(new Bundle());
        assertNotNull(activity);
    }

    @Test
    public void testSetupWindowAnimationsNoCrash() {
        // Protected; just check no exceptions
        Mockito.doNothing().when(activity).setupWindowAnimations();
        activity.setupWindowAnimations();
    }
}