package mohak.uberux;

import org.junit.Test;

import static org.junit.Assert.*;

public class getPolylineTest {

    @Test
    public void testDecodePoly_returnsCorrectSize() {
        getPolyline poly = new getPolyline();
        // polyline encoding for [(38.5, -120.2), (40.7, -120.95), (43.252, -126.453)]
        String encoded = "_p~iF~ps|U_ulLnnqC_mqNvxq`@";
        assertEquals(3, poly.decodePoly(encoded).size());
    }

    @Test
    public void testDecodePoly_emptyString() {
        getPolyline poly = new getPolyline();
        assertEquals(0, poly.decodePoly("").size());
    }
}