package com.example.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

// Simulated widget and settings for Java translation.
class GoogleMapsAddressWidget {
    public String render(String name, String value, java.util.Map<String, Object> attrs) {
        StringBuilder input = new StringBuilder("<input");
        for (var e : attrs.entrySet()) {
            input.append(" ").append(e.getKey()).append("=\"").append(e.getValue().toString()).append("\"");
        }
        input.append(" name=\"").append(name).append("\" type=\"text\"");
        if (value != null) {
            input.append(" value=\"").append(value).append("\"");
        }
        input.append(" />");
        input.append("<div class=\"map_canvas_wrapper\">");
        input.append("<div id=\"map_canvas\"></div></div>");
        return input.toString();
    }

    public Media Media() {
        return new Media();
    }

    public static class Media {
        // Simulate js property; for the test we place key at index 1
        public String[] js = new String[] {
            "other.js",
            "https://maps.google.com/maps/api/js?key=MYKEY&libraries=places"
        };
    }
}

class Settings {
    public static final String GOOGLE_MAPS_API_KEY = "MYKEY";
}

public class WidgetTests {
    @Test
    void testRenderReturnsXxxxxxx() {
        GoogleMapsAddressWidget widget = new GoogleMapsAddressWidget();
        String results = widget.render("name", "value", java.util.Map.of("a1", 1, "a2", 2));
        String expected = "<input a1=\"1\" a2=\"2\" name=\"name\" type=\"text\" value=\"value\" />";
        expected += "<div class=\"map_canvas_wrapper\">";
        expected += "<div id=\"map_canvas\"></div></div>";
        assertHTMLSimilar(expected, results);
    }

    @Test
    void testRenderReturnsBlankForValueWhenNone() {
        GoogleMapsAddressWidget widget = new GoogleMapsAddressWidget();
        String results = widget.render("name", null, java.util.Map.of("a1", 1, "a2", 2));
        String expected = "<input a1=\"1\" a2=\"2\" name=\"name\" type=\"text\" />";
        expected += "<div class=\"map_canvas_wrapper\">";
        expected += "<div id=\"map_canvas\"></div></div>";
        assertHTMLSimilar(expected, results);
    }

    @Test
    void testMapsJsUsesApiKey() {
        GoogleMapsAddressWidget widget = new GoogleMapsAddressWidget();
        String googleMapsJs = "https://maps.google.com/maps/api/js?key=" + Settings.GOOGLE_MAPS_API_KEY + "&libraries=places";
        assertEquals(googleMapsJs, widget.Media().js[1]);
    }

    // Approximate HTML string comparison (ignores whitespace)
    static void assertHTMLSimilar(String expected, String actual) {
        String a = expected.replaceAll("\\s+", "");
        String b = actual.replaceAll("\\s+", "");
        assertEquals(a, b, "HTML content is not equivalent");
    }
}