#include <gtest/gtest.h>
#include <string>

struct StringField {
    std::string get_mikrotik_value(const std::string& v) {return v;}
    std::string get_python_value(const std::string& v) {return v;}
};
struct BytesField {
    std::string get_mikrotik_value(const std::string& v) {return v;}
    std::string get_python_value(const std::string& v) {return v;}
};
struct BooleanField {
    std::string get_mikrotik_value(bool v) { return v ? "yes" : "no"; }
    bool get_python_value(const std::string& v) {
        if (v=="yes"||v=="true") return true;
        if (v=="no"||v=="false") return false;
        throw std::logic_error("bad val");
    }
};
TEST(test_string_field_different_string, works) {
    StringField f; std::string s="hello world!"; EXPECT_EQ(f.get_mikrotik_value(s),s); EXPECT_EQ(f.get_python_value(s),s);
}
TEST(test_boolean_field_variants, works) {
    BooleanField f; EXPECT_EQ(f.get_mikrotik_value(true),"yes"); EXPECT_EQ(f.get_mikrotik_value(false),"no"); EXPECT_TRUE(f.get_python_value("true")); EXPECT_FALSE(f.get_python_value("no"));
}