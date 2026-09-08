package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

class GoogleMapsAddressWidgetPublic {
    public String render(String name, String value, Map<String, Object> attrs) {
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
        public String[] js = new String[] {
                "other.js",
                "https://maps.google.com/maps/api/js?key=PUBLICKEY&libraries=places"
        };
    }
}

class SettingsPublic {
    public static final String GOOGLE_MAPS_API_KEY = "PUBLICKEY";
}

public class WidgetPublicTests {
    static void assertHTMLSimilar(String expected, String actual) {
        String a = expected.replaceAll("\\s+", "");
        String b = actual.replaceAll("\\s+", "");
        assertEquals(a, b, "HTML content is not equivalent");
    }

    @Test
    void testRenderReturnsCustomHtml() {
        GoogleMapsAddressWidgetPublic widget = new GoogleMapsAddressWidgetPublic();
        String results = widget.render("adam", "customvalue", Map.of("id", "unique", "class", "css-test"));
        String expected = "<input id=\"unique\" class=\"css-test\" name=\"adam\" type=\"text\" value=\"customvalue\" />";
        expected += "<div class=\"map_canvas_wrapper\">";
        expected += "<div id=\"map_canvas\"></div></div>";
        assertHTMLSimilar(expected, results);
    }

    @Test
    void testRenderReturnsBlankForValueWhenNonePublic() {
        GoogleMapsAddressWidgetPublic widget = new GoogleMapsAddressWidgetPublic();
        String results = widget.render("foo", null, Map.of("style", "color:red;", "data-bar", "hello"));
        String expected = "<input style=\"color:red;\" data-bar=\"hello\" name=\"foo\" type=\"text\" />";
        expected += "<div class=\"map_canvas_wrapper\">";
        expected += "<div id=\"map_canvas\"></div></div>";
        assertHTMLSimilar(expected, results);
    }

    @Test
    void testMapsJsApiKeyDifferent() {
        GoogleMapsAddressWidgetPublic widget = new GoogleMapsAddressWidgetPublic();
        String googleMapsJs = "https://maps.google.com/maps/api/js?key=" + SettingsPublic.GOOGLE_MAPS_API_KEY + "&libraries=places";
        assertEquals(googleMapsJs, widget.Media().js[1]);
    }
}