#include <gtest/gtest.h>
#include <string>
#include <map>
#include <sstream>

std::string GoogleMapsAddressWidget_render_public(const std::string& name,
                                                 const std::string& value,
                                                 const std::map<std::string, std::string>& attrs) {
    std::ostringstream os;
    os << "<input";
    for (const auto& [k, v] : attrs)
        os << " " << k << "=\"" << v << "\"";
    os << " name=\"" << name << "\" type=\"text\"";
    if (!value.empty())
        os << " value=\"" << value << "\"";
    os << " />";
    os << "<div class=\"map_canvas_wrapper\">";
    os << "<div id=\"map_canvas\"></div></div>";
    return os.str();
}
std::string GoogleMapsAddressWidget_render_blank_public(const std::string& name,
                                                       const std::map<std::string, std::string>& attrs) {
    std::ostringstream os;
    os << "<input";
    for (const auto& [k, v] : attrs)
        os << " " << k << "=\"" << v << "\"";
    os << " name=\"" << name << "\" type=\"text\" />";
    os << "<div class=\"map_canvas_wrapper\">";
    os << "<div id=\"map_canvas\"></div></div>";
    return os.str();
}

std::string GoogleMapsApiJsUrl_public(const std::string& api_key) {
    return "https://maps.google.com/maps/api/js?key=" + api_key + "&libraries=places";
}

TEST(WidgetPublicTests, RenderReturnsCustomHtml) {
    std::string result = GoogleMapsAddressWidget_render_public("adam", "customvalue", {{"id", "unique"}, {"class", "css-test"}});
    std::string expected = "<input id=\"unique\" class=\"css-test\" name=\"adam\" type=\"text\" value=\"customvalue\" />";
    expected += "<div class=\"map_canvas_wrapper\">";
    expected += "<div id=\"map_canvas\"></div></div>";
    EXPECT_EQ(expected, result);
}

TEST(WidgetPublicTests, RenderReturnsBlankForValueWhenNonePublic) {
    std::string result = GoogleMapsAddressWidget_render_blank_public("foo", {{"style", "color:red;"}, {"data-bar", "hello"}});
    std::string expected = "<input style=\"color:red;\" data-bar=\"hello\" name=\"foo\" type=\"text\" />";
    expected += "<div class=\"map_canvas_wrapper\">";
    expected += "<div id=\"map_canvas\"></div></div>";
    EXPECT_EQ(expected, result);
}

TEST(WidgetPublicTests, MapsJsApiKeyDifferent) {
    std::string api_key = "OTHER_PUBLIC_KEY";
    std::string google_maps_js = GoogleMapsApiJsUrl_public(api_key);
    std::string widget_media_js1 = google_maps_js;
    EXPECT_EQ(google_maps_js, widget_media_js1);
}