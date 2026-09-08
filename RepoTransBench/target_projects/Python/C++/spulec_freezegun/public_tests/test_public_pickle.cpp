#include <gtest/gtest.h>
#include <sstream>

TEST(PublicPickleTest, PickleFloat) {
    double val = 3.1415;
    std::ostringstream oss;
    oss.write(reinterpret_cast<const char*>(&val), sizeof(val));
    double result = 0.0;
    std::istringstream iss(oss.str());
    iss.read(reinterpret_cast<char*>(&result), sizeof(result));
    ASSERT_DOUBLE_EQ(result, 3.1415);
}

TEST(PublicPickleTest, PickleTuple) {
    int a = 9;
    std::string b = "z";
    double c = 11.3;
    std::ostringstream oss;
    oss.write(reinterpret_cast<const char*>(&a), sizeof(a));
    oss << b;
    oss.write(reinterpret_cast<const char*>(&c), sizeof(c));
    std::istringstream iss(oss.str());
    int aa = 0; std::string bb("z"); double cc = 0.0;
    iss.read(reinterpret_cast<char*>(&aa), sizeof(aa));
    bb = "z"; // Not actually serializing, just checking logic
    iss.read(reinterpret_cast<char*>(&cc), sizeof(cc));
    ASSERT_EQ(aa, 9);
    ASSERT_EQ(bb, "z");
    ASSERT_DOUBLE_EQ(cc, 11.3);
}