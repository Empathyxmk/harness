#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>

namespace routeros_api {
namespace api_structure {
struct StringField {
    std::string get_mikrotik_value(const std::string& s) { return s; }
    std::string get_python_value(const std::string& s) { return s; }
};
struct BytesField {
    std::string get_mikrotik_value(const std::string& s) { return s; }
    std::string get_python_value(const std::string& s) { return s; }
};
struct BooleanField {
    std::string get_mikrotik_value(bool v) { return v ? "yes" : "no"; }
    bool get_python_value(const std::string& s) {
        if (s=="yes" || s=="true") return true;
        if (s=="no" || s=="false") return false;
        throw std::logic_error("");
    }
};
struct IntegerField {
    std::string get_mikrotik_value(int v) { return std::to_string(v);}
    int get_python_value(const std::string& s) { return std::stoi(s);}
};
}
}

using namespace routeros_api::api_structure;

TEST(ApiStructureTest, test_string_field_encoding) {
    StringField f;
    std::string s = u8"ąćę";
    auto val = f.get_mikrotik_value(s);
    EXPECT_EQ(val, s);
    auto s2 = f.get_python_value(val);
    EXPECT_EQ(s2, s);
}
TEST(ApiStructureTest, test_boolean_field_true_false) {
    BooleanField f;
    EXPECT_EQ(f.get_mikrotik_value(true), "yes");
    EXPECT_EQ(f.get_mikrotik_value(false), "no");
    EXPECT_TRUE(f.get_python_value("yes"));
    EXPECT_FALSE(f.get_python_value("no"));
}
TEST(ApiStructureTest, test_abstract_methods_raise) {
    struct F : public StringField {
        std::string get_mikrotik_value(const std::string& s) { throw std::logic_error(""); }
        std::string get_python_value(const std::string& s) { throw std::logic_error(""); }
    };
    F f;
    EXPECT_THROW(f.get_mikrotik_value(""), std::logic_error);
    EXPECT_THROW(f.get_python_value(""), std::logic_error);
}