#include <gtest/gtest.h>
#include <tuple>
#include <string>
#include "lib/geo_pt_field.h"
#include "lib/address_fields.h"
#include "lib/widgets.h"

// DummyModel not used

TEST(GeoPtFieldTests, ToPythonAndGetPrepValue) {
    GeoPtField f;
    EXPECT_EQ(std::make_tuple(40.1, -122.1), f.to_python("40.1,-122.1"));
    EXPECT_EQ("10,20", f.get_prep_value(std::make_tuple(10.0, 20.0)));
    EXPECT_EQ("50.33,80.55", f.get_prep_value("50.33,80.55"));
    // Error case
    EXPECT_THROW(f.to_python("badinput"), std::exception);
}

TEST(AddressFieldTests, GeolocationDeconstructAndOther) {
    DummyAddressField f(100);
    EXPECT_EQ("DummyAddressField", f.str());
    EXPECT_EQ("DummyAddressField(max_length=100)", f.repr());
}
TEST(AddressFieldTests, GeoLocationFieldMemberTest) {
    DummyLocationField latlng(50);
    EXPECT_EQ("DummyLocationField", latlng.str());
    EXPECT_EQ("DummyLocationField(max_length=50)", latlng.repr());
}

TEST(AddressFieldTests, AddressAndLocationFieldReprStr) {
    DummyAddressField af(255);
    DummyLocationField lf(255);
    EXPECT_EQ("DummyAddressField", af.str());
    EXPECT_EQ("DummyLocationField", lf.str());
    EXPECT_EQ("DummyAddressField(max_length=255)", af.repr());
    EXPECT_EQ("DummyLocationField(max_length=255)", lf.repr());
}

TEST(WidgetsTest, RenderAttrsInstantiation) {
    DummyMapWidget map_widget({{"id", "some_id"}});
    std::string html = map_widget.render("test", "value", {{"id","some_id"}});
    EXPECT_TRUE(html.find("id") != std::string::npos || html.find("map") != std::string::npos);
}

TEST(GeoPtFieldTests, CustomCleanValidation) {
    DummyGeoPtField f;
    // A function that throws to simulate error
    EXPECT_THROW(f.clean("badstring"), std::exception);
}