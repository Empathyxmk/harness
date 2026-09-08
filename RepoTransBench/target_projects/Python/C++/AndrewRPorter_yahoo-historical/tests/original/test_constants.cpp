#include <gtest/gtest.h>
#include "yahoo_historical_constants_stub.h"
#include <string>
#include <typeinfo>
#include <set>

TEST(ConstantsTest, ConstantsImport) {
    using namespace Constants;
    (void)API_URL;
    (void)DATE_INTERVALS;
    (void)ONE_DAY_INTERVAL;
}
TEST(ConstantsTest, UrlDictOrList) {
    using namespace Constants;
    EXPECT_GT(DATE_INTERVALS.size(), 0);
    for (const auto& val : DATE_INTERVALS) {
        EXPECT_EQ(typeid(val), typeid(std::string));
    }
}
TEST(ConstantsTest, ConstantValues) {
    using namespace Constants;
    EXPECT_EQ(typeid(API_URL), typeid(std::string));
    EXPECT_EQ(typeid(ONE_DAY_INTERVAL), typeid(std::string));
    EXPECT_EQ(typeid(DATE_INTERVALS), typeid(std::set<std::string>));
}
TEST(ConstantsTest, ConstantModuleStr) {
    using namespace Constants;
    std::string mod_str = API_URL;
    std::string repr = API_URL;
    EXPECT_EQ(typeid(mod_str), typeid(std::string));
    EXPECT_EQ(typeid(repr), typeid(std::string));
}
TEST(ConstantsTest, AllConstantSymbolsAccounted) {
    using namespace Constants;
    EXPECT_EQ(typeid(API_URL), typeid(std::string));
    EXPECT_EQ(typeid(DATE_INTERVALS), typeid(std::set<std::string>));
    EXPECT_EQ(typeid(ONE_DAY_INTERVAL), typeid(std::string));
}
TEST(ConstantsTest, ModuleDirSubset) {
    // In C++: simulate module "dir" by presence in namespace
    using namespace Constants;
    EXPECT_EQ(typeid(API_URL), typeid(std::string));
}