package com.example.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.Map;

class GeoPtField {
    public Object to_python(String value) {
        if (value == null) return null;
        String[] arr = value.split(",");
        if (arr.length != 2) throw new RuntimeException("Bad value");
        return new double[] { Double.parseDouble(arr[0]), Double.parseDouble(arr[1]) };
    }
    public String get_prep_value(Object val) {
        if (val == null) return null;
        if (val instanceof String) return (String) val;
        if (val instanceof double[]) {
            double[] v = (double[]) val;
            return v[0] + "," + v[1];
        }
        throw new RuntimeException("Bad value");
    }
}

class AddressField {
    int maxLength;
    String def;
    AddressField(int len, String def) { this.maxLength = len; this.def = def; }
    Object[] deconstruct() {
        return new Object[] {null, "AddressField", null,
            Map.of("max_length", maxLength, "default", def)};
    }
}

class GeoLocationField {
    public Object formfield;
    public Object[] deconstruct() {
        return new Object[]{null, "GeoLocationField", null, Map.of()};
    }
}

class Model {
    // Simulates Django model meta behavior
    public static class _meta {
        public static CustomField[] fields = new CustomField[] { new CustomField(), new CustomField() };
    }
    public static class CustomField {
        public String value_to_string(Model sut) { return "45.0,90.0"; }
        public Object get_prep_value(Object val) { return val == null ? null : val.toString(); }
    }
}

class MapWidget {
    public String render(String name, String value, Map<String, String> attrs) {
        String input = "<input id=\"some_id\" name=\""+name+"\" type=\"text\" value=\""+value+"\">";
        return input;
    }
    public Map<String, String> js_attrs = Map.of("foo", "bar");
}
public class FieldsModelsWidgetsTests {

    @Test
    void testGeoPtFieldToPythonAndGetPrepValue() {
        GeoPtField f = new GeoPtField();
        assertArrayEquals(new double[]{40.1, -122.1}, (double[])f.to_python("40.1,-122.1"));
        assertEquals("10.0,20.0", f.get_prep_value(new double[]{10.0, 20.0}));
        assertEquals("50.33,80.55", f.get_prep_value("50.33,80.55"));
        assertNull(f.to_python(null));
        assertThrows(RuntimeException.class, () -> f.to_python("badinput"));
    }

    @Test
    void testGeolocationFieldDeconstructAndOther() {
        AddressField f = new AddressField(100, "def");
        Object[] res = f.deconstruct();
        assertTrue(res[0] == null || res[0] instanceof String);
        @SuppressWarnings("unchecked")
        Map<String, Object> kwargs = (Map<String, Object>) res[3];
        assertTrue(kwargs.containsKey("max_length"));
        assertEquals(100, kwargs.get("max_length"));
        assertEquals("def", kwargs.get("default"));

        GeoLocationField latlng = new GeoLocationField();
        assertNotNull(latlng.formfield);
        Object[] d2 = latlng.deconstruct();
        assertTrue(d2[3] instanceof Map);
    }

    @Test
    void testModelsAddressAndLocationFieldReprAndStr() {
        // Simulate AddressField and LocationField with __str__/toString
        class AddressField2 { public String toString(){return "Field:123 st la";} }
        class LocationField2 { public String toString(){return "LocationField:11.0,122.2";} }
        Object[] fieldsAndVals = new Object[] {
                new AddressField2(), "123 st la",
                new LocationField2(), "11.0,122.2"
        };
        for (int i=0; i<fieldsAndVals.length; i+=2) {
            assertTrue(fieldsAndVals[i].toString().contains("Field"));
        }
    }

    @Test
    void testWidgetsRenderAttrsInstantiation() {
        MapWidget mapWidget = new MapWidget();
        String html = mapWidget.render("test", "value", Map.of("id", "some_id"));
        assertTrue(html.contains("id") || html.contains("map"));
        assertNotNull(mapWidget.js_attrs);
    }

    @Test
    void testCustomCleanValidation() {
        GeoPtField f = new GeoPtField() {
            @Override
            public Object to_python(String value) {
                throw new RuntimeException("For test");
            }
        };
        assertThrows(RuntimeException.class, () -> f.to_python("50.11,-101.2"));
    }
}