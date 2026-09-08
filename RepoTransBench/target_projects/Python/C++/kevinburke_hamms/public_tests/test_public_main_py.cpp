#include <gtest/gtest.h>
#include <string>

TEST(PublicMainPy, MainTrue) {
    ASSERT_TRUE(std::vector<int>{1}.size() > 0);
}

TEST(PublicMainPy, MainValueType) {
    std::string val = "hamms";
    ASSERT_TRUE(typeid(val) == typeid(std::string));
}