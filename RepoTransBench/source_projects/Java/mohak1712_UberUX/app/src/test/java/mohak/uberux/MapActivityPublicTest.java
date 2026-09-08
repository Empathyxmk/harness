package mohak.uberux;

import android.os.Bundle;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.junit.Assert.*;

public class MapActivityPublicTest {

    private MapActivity activity;

    @Before
    public void setUp() {
        activity = Mockito.mock(MapActivity.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testOnCreateExecutesWithoutCrash_public() {
        Bundle bundle = new Bundle();
        bundle.putDouble("public_test_double", 88.88d);
        activity.onCreate(bundle);
        assertNotNull(activity);
    }
}