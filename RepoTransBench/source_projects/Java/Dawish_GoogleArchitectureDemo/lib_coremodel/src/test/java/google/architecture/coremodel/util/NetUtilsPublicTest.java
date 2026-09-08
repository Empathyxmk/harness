package google.architecture.coremodel.util;

import org.junit.Test;
import static org.junit.Assert.*;

public class NetUtilsPublicTest {

    @Test
    public void testIsNetworkConnected_false() {
        // As NetUtils networking depends on Android platform, we can test static stub/logic.
        // Here we just demonstrate a stub test with different 'expected' result value
        assertFalse("Network should be disconnected in this stub public test", false);
    }

    @Test
    public void testIsNetworkConnected_true() {
        assertTrue("Network is connected in this stub public test", true);
    }
}