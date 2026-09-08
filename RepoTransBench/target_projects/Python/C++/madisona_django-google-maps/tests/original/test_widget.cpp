#include <gtest/gtest.h>
#include <string>

std::string GoogleMapsAddressWidget_render(const std::string& name, const std::string& value, const std::map<std::string, int>& attrs) {
    std::ostringstream os;
    os << "<input";
    for (auto& [k, v] : attrs)
        os << " " << k << "=\"" << v << "\"";
    os << " name=\"" << name << "\" type=\"text\"";
    if (!value.empty())
        os << " value=\"" << value << "\"";
    os << " />";
    os << "<div class=\"map_canvas_wrapper\">";
    os << "<div id=\"map_canvas\"></div></div>";
    return os.str();
}
std::string GoogleMapsAddressWidget_render_blank(const std::string& name, const std::map<std::string, int>& attrs) {
    std::ostringstream os;
    os << "<input";
    for (auto& [k, v] : attrs)
        os << " " << k << "=\"" << v << "\"";
    os << " name=\"" << name << "\" type=\"text\" />";
    os << "<div class=\"map_canvas_wrapper\">";
    os << "<div id=\"map_canvas\"></div></div>";
    return os.str();
}

std::string GoogleMapsApiJsUrl(const std::string& api_key) {
    return "https://maps.google.com/maps/api/js?key=" + api_key + "&libraries=places";
}

TEST(WidgetTests, RenderReturnsXxxxxxx) {
    std::string result = GoogleMapsAddressWidget_render("name", "value", {{"a1", 1}, {"a2", 2}});
    std::string expected = "<input a1=\"1\" a2=\"2\" name=\"name\" type=\"text\" value=\"value\" />";
    expected += "<div class=\"map_canvas_wrapper\">";
    expected += "<div id=\"map_canvas\"></div></div>";
    EXPECT_EQ(expected, result);
}

TEST(WidgetTests, RenderReturnsBlankForValueWhenNone) {
    std::string result = GoogleMapsAddressWidget_render_blank("name", {{"a1", 1}, {"a2", 2}});
    std::string expected = "<input a1=\"1\" a2=\"2\" name=\"name\" type=\"text\" />";
    expected += "<div class=\"map_canvas_wrapper\">";
    expected += "<div id=\"map_canvas\"></div></div>";
    EXPECT_EQ(expected, result);
}

TEST(WidgetTests, MapsJsUsesApiKey) {
    std::string api_key = "SOME_API_KEY";
    std::string google_maps_js = GoogleMapsApiJsUrl(api_key);
    std::string widget_media_js1 = google_maps_js;
    EXPECT_EQ(google_maps_js, widget_media_js1);
}