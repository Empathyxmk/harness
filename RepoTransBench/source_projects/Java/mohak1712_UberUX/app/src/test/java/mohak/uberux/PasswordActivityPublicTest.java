package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.junit.Assert.*;

public class PasswordActivityPublicTest {
    private PasswordActivity activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(PasswordActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreateExecutesWithoutCrash_public() {
        Bundle bundle = new Bundle();
        bundle.putChar("public_test_char", 'P');
        activity.onCreate(bundle);
        assertNotNull(activity);
    }
}