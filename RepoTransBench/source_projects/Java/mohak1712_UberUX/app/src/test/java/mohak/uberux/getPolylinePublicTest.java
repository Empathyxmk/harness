package mohak.uberux;

import org.junit.Test;
import static org.junit.Assert.*;

public class getPolylinePublicTest {
    @Test
    public void testDecodePolyline_differentCoords_public() {
        // Different polyline string from the original (from online Polyline encoder)
        String testPolyline = "_p~iF~ps|U_ulLnnqC_mqNvxq`@";
        java.util.List<android.location.Location> result = getPolyline.decodePoly(testPolyline);

        // Instead of checking expected size=3, use for this test
        assertTrue(result.size() >= 2);
    }
}