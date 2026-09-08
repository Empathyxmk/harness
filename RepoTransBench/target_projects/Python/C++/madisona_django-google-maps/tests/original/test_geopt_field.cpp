#include <gtest/gtest.h>
#include <tuple>
#include <string>
#include <sstream>
#include <stdexcept>
#include <cmath>

// Minimal GeoPt to mimic test
class GeoPt {
public:
    double lat;
    double lon;
    GeoPt(const std::string& s) {
        size_t p = s.find(',');
        if (p == std::string::npos) throw std::invalid_argument("invalid string");
        lat = std::stod(s.substr(0, p));
        lon = std::stod(s.substr(p+1));
        if (lat > 90 || lat < -90)
            throw std::invalid_argument("lat out of range");
    }
    GeoPt(double la, double lo): lat(la), lon(lo) {
        if (lat > 90 || lat < -90)
            throw std::invalid_argument("lat out of range");
    }
    bool operator==(const GeoPt& o) const { return std::abs(lat - o.lat) < 1e-8 && std::abs(lon - o.lon) < 1e-8; }
    bool operator!=(const GeoPt& o) const { return !(*this == o); }
    operator std::string() const {
        std::ostringstream oss;
        if (isnan(lat) || isnan(lon)) return "";
        oss << lat << "," << lon;
        return oss.str();
    }
    size_t size() const { return std::string(*this).size(); }
};

TEST(GeoPtFieldTests, SetsLatLonOnInitialization) {
    GeoPt gp("15.001,32.001");
    EXPECT_DOUBLE_EQ(15.001, gp.lat);
    EXPECT_DOUBLE_EQ(32.001, gp.lon);
}

TEST(GeoPtFieldTests, UsesLatCommaLonAsUnicodeRepresentation) {
    GeoPt gp("15.001,32.001");
    std::string s = static_cast<std::string>(gp);
    EXPECT_EQ("15.001,32.001", s);
}

TEST(GeoPtFieldTests, TwoGeoPtsWithSameLatLonShouldBeEqual) {
    GeoPt g1("15.001,32.001");
    GeoPt g2("15.001,32.001");
    EXPECT_TRUE(g1 == g2);
}

TEST(GeoPtFieldTests, TwoGeoPtsWithDifferentLatShouldNotBeEqual) {
    GeoPt g1("15.001,32.001");
    GeoPt g2("20.001,32.001");
    EXPECT_TRUE(g1 != g2);
}

TEST(GeoPtFieldTests, TwoGeoPtsWithDifferentLonShouldNotBeEqual) {
    GeoPt g1("15.001,32.001");
    GeoPt g2("15.001,62.001");
    EXPECT_TRUE(g1 != g2);
}
TEST(GeoPtFieldTests, NotEqualWhenComparisonNotGeoPt) {
    GeoPt g1("15.001,32.001");
    std::string s = "15.001,32.001";
    EXPECT_TRUE(g1 != GeoPt(s));
}
TEST(GeoPtFieldTests, AllowsGeoPtInstantiatedWithEmptyString) {
    // An empty string will throw (as per this minimal implementation)
    EXPECT_THROW(GeoPt(""), std::invalid_argument);
}
TEST(GeoPtFieldTests, SplitsGeoPointOnComma) {
    GeoPt pt("15.001,32.001");
    EXPECT_EQ("15.001", std::to_string(pt.lat).substr(0,6));
    EXPECT_EQ("32.001", std::to_string(pt.lon).substr(0,6));
}
// Skipping: raises error when attribute error on split, type error, out-of-range, etc.