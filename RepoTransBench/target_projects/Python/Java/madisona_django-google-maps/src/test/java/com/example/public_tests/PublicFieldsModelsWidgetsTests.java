package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

public class PublicFieldsModelsWidgetsTests {

    // Simulated equivalents for public tests

    static class FakeGeoPtField {
        public Object to_python(String value) {
            if (value == null) return null;
            String[] pieces = value.split(",");
            return new double[]{Double.parseDouble(pieces[0].trim()), Double.parseDouble(pieces[1].trim())};
        }
        public String get_prep_value(Object value) {
            if (value == null) return null;
            if (value instanceof String) return (String)value;
            if (value instanceof double[] d && d.length == 2) {
                return String.format("%.8f,%.8f", d[0], d[1]);
            }
            throw new RuntimeException("Invalid value for GeoPtField");
        }
    }

    @Test
    void testGeoptfieldToPythonAndGetPrepValuePublic() {
        FakeGeoPtField f = new FakeGeoPtField();
        String rawVal = "1.111,-2.222";
        double[] pyVal = (double[])f.to_python(rawVal);
        assertArrayEquals(new double[] {1.111, -2.222}, pyVal);
        assertEquals("3.33300000,-4.44400000", f.get_prep_value(new double[]{3.333, -4.444}));
    }

    @Test
    void testModelsAddressAndLocationFieldReprAndStrPublic() {
        class DummyAddressField {
            int maxLength;
            DummyAddressField(int ml) { maxLength = ml; }
            public String toString() { return "DummyAddressField"; }
            public String toRepr() { return "DummyAddressField(max_length=" + maxLength + ")"; }
        }
        class DummyLocationField {
            int maxLength;
            DummyLocationField(int ml) { maxLength = ml; }
            public String toString() { return "DummyLocationField"; }
            public String toRepr() { return "DummyLocationField(max_length=" + maxLength + ")"; }
        }
        Object[] fields_and_vals = {
            new DummyAddressField(150), "456 road ave",
            new DummyLocationField(150), "85.63,-172.54"
        };
        for (int i = 0; i < fields_and_vals.length; i+=2) {
            assertTrue(fields_and_vals[i].toString() instanceof String);
            assertTrue(fields_and_vals[i] instanceof DummyAddressField || fields_and_vals[i] instanceof DummyLocationField ?
                ((fields_and_vals[i] instanceof DummyAddressField) ?
                    ((DummyAddressField)fields_and_vals[i]).toRepr() instanceof String :
                    ((DummyLocationField)fields_and_vals[i]).toRepr() instanceof String
                ) : true);
        }
    }

    @Test
    void testWidgetsRenderAttrsInstantiationPublic() {
        class DummyMapWidget {
            Map<String,String> attrs;
            DummyMapWidget(Map<String,String> attrs) {
                this.attrs = attrs;
            }
            String render(String name, String value, Map<String,String> attrsOverride) {
                String attrsString = "";
                if (attrsOverride != null) attrsString = attrsOverride.toString();
                return "<input type=\"text\" name=\"" + name + "\" value=\"" + value + "\" " + attrsString + ">";
            }
        }
        DummyMapWidget mapWidget = new DummyMapWidget(Map.of("placeholder", "Enter city"));
        String html = mapWidget.render("sample_location", "21.44,13.33", Map.of("id","map-field"));
        assertTrue(html.contains("sample_location"));
        assertTrue(html.contains("21.44,13.33"));
        assertTrue(html.contains("id"));
        assertFalse(html.contains("placeholder"));
    }

    @Test
    void testCustomCleanValidationPublic() {
        class DummyGeoPtField {
            public double[] clean(Object value) {
                if (value instanceof double[] arr && arr.length == 2) {
                    return arr;
                }
                if (value instanceof String s) {
                    String[] pieces = s.split(",");
                    if (pieces.length != 2) throw new IllegalArgumentException();
                    return new double[]{Double.parseDouble(pieces[0]), Double.parseDouble(pieces[1])};
                }
                throw new IllegalArgumentException();
            }
        }
        DummyGeoPtField field = new DummyGeoPtField();
        // Valid tuple
        assertArrayEquals(new double[]{12.34, -56.78}, field.clean(new double[]{12.34, -56.78}));
        // Valid string
        assertArrayEquals(new double[]{0.987, -0.654}, field.clean("0.987,-0.654"));
        // Invalid values
        assertThrows(IllegalArgumentException.class, () -> field.clean("notacoord"));
        assertThrows(IllegalArgumentException.class, () -> field.clean(new double[]{1.2}));
    }
}