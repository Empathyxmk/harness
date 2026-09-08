#include <gtest/gtest.h>
#include <string>
#include <sstream>

TEST(PickleTest, PickleFloat) {
    double val = 3.1415;
    std::ostringstream oss;
    oss.write(reinterpret_cast<const char*>(&val), sizeof(val));
    double result = 0.0;
    std::istringstream iss(oss.str());
    iss.read(reinterpret_cast<char*>(&result), sizeof(result));
    ASSERT_DOUBLE_EQ(result, 3.1415);
}