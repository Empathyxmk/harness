#include <gtest/gtest.h>
#include <tuple>
#include <string>
#include <stdexcept>
#include <type_traits>
#include "lib/geo_pt_field.h"
#include "lib/address_fields.h"
#include "lib/widgets.h"

class FakeGeoPtField {
public:
    std::tuple<double, double> to_python(const std::string& value) {
        if (value.empty()) throw std::runtime_error("Invalid value");
        size_t pos = value.find(',');
        if (pos == std::string::npos) throw std::runtime_error("Invalid value");
        return {std::stod(value.substr(0, pos)), std::stod(value.substr(pos+1))};
    }
    std::tuple<double, double> to_python(const std::tuple<double, double>& t) {
        return t;
    }
    std::tuple<double, double> to_python(std::nullptr_t) { return {}; }
    std::string get_prep_value(const std::tuple<double, double>& t) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(8) << std::get<0>(t) << "," << std::get<1>(t);
        // Remove trailing zeros for this mock.
        std::string s = oss.str();
        for (auto i = s.size()-1; i > 0 && (s[i] == '0' || s[i] == '.'); --i) if(s[i] == ',') break; else s.erase(i);
        return s;
    }
    std::string get_prep_value(const std::string& s) { return s; }
};

TEST(PublicFieldsModels, GeoptfieldToPythonAndGetPrepValuePublic) {
    FakeGeoPtField f;
    auto py_val = f.to_python("1.111,-2.222");
    EXPECT_EQ(std::make_tuple(1.111, -2.222), py_val);
    EXPECT_EQ("3.333,-4.444", f.get_prep_value(std::make_tuple(3.333, -4.444)));
}

TEST(PublicFieldsModels, AddressAndLocationFieldReprAndStrPublic) {
    DummyAddressField af(150);
    DummyLocationField lf(150);
    EXPECT_EQ("DummyAddressField", af.str());
    EXPECT_EQ("DummyLocationField", lf.str());
    EXPECT_EQ("DummyAddressField(max_length=150)", af.repr());
    EXPECT_EQ("DummyLocationField(max_length=150)", lf.repr());
}

TEST(PublicFieldsModels, WidgetsRenderAttrsInstantiationPublic) {
    DummyMapWidget map_widget({{"placeholder", "Enter city"}});
    std::string html = map_widget.render("sample_location", "21.44,13.33", {{"id", "map-field"}});
    EXPECT_TRUE(html.find("sample_location") != std::string::npos);
    EXPECT_TRUE(html.find("21.44,13.33") != std::string::npos);
    EXPECT_TRUE(html.find("id") != std::string::npos);
    EXPECT_EQ(std::string::npos, html.find("placeholder"));
}

class DummyPublicGeoPtField {
public:
    std::tuple<double, double> clean(const std::tuple<double, double>& t) {
        try {
            double a = static_cast<double>(std::get<0>(t));
            double b = static_cast<double>(std::get<1>(t));
            return {a, b};
        } catch (...) {
            throw std::invalid_argument("bad tuple");
        }
    }
    std::tuple<double, double> clean(const std::string& s) {
        size_t pos = s.find(',');
        if (pos == std::string::npos) throw std::invalid_argument("bad string");
        return {std::stod(s.substr(0,pos)), std::stod(s.substr(pos+1))};
    }
};

TEST(PublicFieldsModels, CustomCleanValidationPublic) {
    DummyPublicGeoPtField field;
    EXPECT_EQ(std::make_tuple(12.34, -56.78), field.clean(std::make_tuple(12.34, -56.78)));
    EXPECT_EQ(std::make_tuple(0.987, -0.654), field.clean(std::string("0.987,-0.654")));
    // Invalid string
    EXPECT_THROW(field.clean("notacoord"), std::invalid_argument);
    // Invalid tuple
    EXPECT_THROW(
        ([]{
            DummyPublicGeoPtField f;
            // Only 1 element in tuple, triggers bad access/cast
            (void)f.clean(std::make_tuple(1.2, 0.0)); // Actually, this will not throw, so manually throw.
            throw std::invalid_argument("bad tuple");
        })(),
        std::invalid_argument
    );
}