package com.example.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

// Minimal version of GeoPt, GeoPtField to test original logic
class GeoPt {
    public Double lat = null;
    public Double lon = null;

    public GeoPt(String v) {
        if (v == null || v.trim().isEmpty()) return;
        String[] parts = v.split(",");
        if (parts.length == 2) {
            try {
                double latitude = Double.parseDouble(parts[0].trim());
                double longitude = Double.parseDouble(parts[1].trim());
                if (latitude <= -180 || latitude >= 180)
                    throw new ValidationException("Latitude out of range");
                this.lat = latitude;
                this.lon = longitude;
            } catch (NumberFormatException ex) {
                throw new ValidationException("Invalid lat/lon");
            }
        } else if (v.isEmpty()) {
            // Handle empty explicitly
        } else {
            throw new ValidationException("Bad input for GeoPt");
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof GeoPt)) return false;
        GeoPt other = (GeoPt) obj;
        if (lat == null || lon == null || other.lat == null || other.lon == null) return false;
        return lat.equals(other.lat) && lon.equals(other.lon);
    }

    @Override
    public String toString() {
        if (lat == null || lon == null) return "";
        return String.format("%.3f,%.3f", lat, lon).replaceAll("\\.000", "");
    }
}

class ValidationException extends RuntimeException {
    public ValidationException(String msg) { super(msg); }
}

public class GeoPtFieldTests {
    @Test
    void testSetsLatLonOnInitialization() {
        GeoPt geoPt = new GeoPt("15.001,32.001");
        assertEquals(15.001, geoPt.lat);
        assertEquals(32.001, geoPt.lon);
    }

    @Test
    void testUsesLatCommaLonAsUnicodeRepresentation() {
        GeoPt geoPt = new GeoPt("15.001,32.001");
        assertEquals("15.001,32.001", geoPt.toString());
    }

    @Test
    void testTwoGeoPtsWithSameLatLonShouldBeEqual() {
        GeoPt pt1 = new GeoPt("15.001,32.001");
        GeoPt pt2 = new GeoPt("15.001,32.001");
        assertEquals(pt1, pt2);
    }

    @Test
    void testTwoGeoPtsWithDifferentLatShouldNotBeEqual() {
        GeoPt pt1 = new GeoPt("15.001,32.001");
        GeoPt pt2 = new GeoPt("20.001,32.001");
        assertNotEquals(pt1, pt2);
    }

    @Test
    void testTwoGeoPtsWithDifferentLonShouldNotBeEqual() {
        GeoPt pt1 = new GeoPt("15.001,32.001");
        GeoPt pt2 = new GeoPt("15.001,62.001");
        assertNotEquals(pt1, pt2);
    }

    @Test
    void testIsNotEqualWhenComparisonIsNotGeoPtObject() {
        GeoPt pt1 = new GeoPt("15.001,32.001");
        String pt2 = "15.001,32.001";
        assertNotEquals(pt1, pt2);
    }

    @Test
    void testAllowsGeoPtInstantiatedWithEmptyString() {
        GeoPt pt = new GeoPt("");
        assertNull(pt.lat);
        assertNull(pt.lon);
    }

    @Test
    void testUsesEmptyStringAsUnicodeRepresentationForEmptyGeoPt() {
        GeoPt pt = new GeoPt("");
        assertEquals("", pt.toString());
    }

    @Test
    void testSplitsGeoPointOnComma() {
        GeoPt pt = new GeoPt("15.001,32.001");
        assertEquals("15.001", String.valueOf(pt.lat));
        assertEquals("32.001", String.valueOf(pt.lon));
    }

    @Test
    void testRaisesErrorWhenAttributeErrorOnSplit() {
        assertThrows(ValidationException.class, () -> {
            new GeoPt((String) null);
        });
    }

    @Test
    void testRaisesErrorWhenTypeErrorOnSplit() {
        assertThrows(ValidationException.class, () -> {
            new GeoPt("x,x");
        });
    }

    @Test
    void testReturnsFloatValueWhenValidValue() {
        GeoPt pt = new GeoPt("45.005,180");
        assertEquals(45.005, pt.lat);
    }

    @Test
    void testRaisesExceptionWhenValueIsOutOfUpperRange() {
        assertThrows(ValidationException.class, () -> {
            new GeoPt("180,180");
        });
    }

    @Test
    void testRaisesExceptionWhenValueIsOutOfLowerRange() {
        assertThrows(ValidationException.class, () -> {
            new GeoPt("-180,180");
        });
    }

    @Test
    void testLenReturnsLenOfUnicodeValue() {
        GeoPt pt = new GeoPt("84,12");
        assertEquals("84,12".length(), pt.toString().length());
    }

    @Test
    void testRaisesExceptionNotEnoughValuesToUnpack() {
        assertThrows(ValidationException.class, () -> {
            new GeoPt("22");
        });
    }

    @Test
    void testRaisesExceptionTooManyValuesToUnpack() {
        assertThrows(ValidationException.class, () -> {
            new GeoPt("22,50,90");
        });
    }
}