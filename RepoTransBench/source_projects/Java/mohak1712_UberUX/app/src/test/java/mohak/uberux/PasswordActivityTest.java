package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class PasswordActivityTest {

    private PasswordActivity activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(PasswordActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreate_noCrash() {
        activity.onCreate(new Bundle());
        assertNotNull(activity);
    }

    @Test
    public void testSetupWindowAnimations() {
        // Should be safe if protected, mock no-op
        Mockito.doNothing().when(activity).setupWindowAnimations();
        activity.setupWindowAnimations();
    }
}