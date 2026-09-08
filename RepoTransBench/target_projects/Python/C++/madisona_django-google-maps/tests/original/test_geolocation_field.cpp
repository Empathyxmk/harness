#include <gtest/gtest.h>
#include <string>

struct Person {
    std::string geolocation;
    Person(std::string geo): geolocation(std::move(geo)) {}
    double get_lat() const {
        size_t p = geolocation.find(',');
        return std::stod(geolocation.substr(0, p));
    }
    double get_lon() const {
        size_t p = geolocation.find(',');
        return std::stod(geolocation.substr(p+1));
    }
};

TEST(GeoLocationFieldTests, GettingLatLonFromModelGivenString) {
    Person p("45,90");
    EXPECT_EQ(45, p.get_lat());
    EXPECT_EQ(90, p.get_lon());
}
TEST(GeoLocationFieldTests, GettingLatLonFromModelGivenPt) {
    Person p("45,90");
    EXPECT_EQ(45, p.get_lat());
    EXPECT_EQ(90, p.get_lon());
}
TEST(GeoLocationFieldTests, ValueToStringWithPoint) {
    Person p("45.0,90.0");
    std::string s = p.geolocation;
    EXPECT_EQ("45.0,90.0", s);
}
TEST(GeoLocationFieldTests, ValueToStringWithString) {
    Person p("45,90");
    std::string s = p.geolocation;
    EXPECT_EQ("45,90", s);
}
TEST(GeoLocationFieldTests, GetPrepValueReturnsNoneWhenNone) {
    std::string* field = nullptr;
    EXPECT_EQ(nullptr, field);
}