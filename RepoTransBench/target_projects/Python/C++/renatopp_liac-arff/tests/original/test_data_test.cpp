#include <gtest/gtest.h>
#include <vector>
#include <string>
#include "arff_cpp.h"

// ConversorStub and COOStub classes must be implemented similarly, here as minimal working C++ mocks:
struct ConversorStub {
    std::function<ARFFValue(const std::string&)> r_value;
    ARFFValue operator()(const std::string& value) { return r_value(value); }
};
struct COOStub {
    std::vector<ARFFValue> data;
    std::vector<int> row, col;
    COOStub(const std::vector<ARFFValue>& d, const std::vector<int>& r, const std::vector<int>& c) : data(d), row(r), col(c) {}
};

class DataTest : public ::testing::Test {
    //...
};
TEST_F(DataTest, test_conversor) {
    std::vector<ConversorStub> conversors;
    conversors.emplace_back([](const std::string& v) { return ARFFValue(v); });
    conversors.emplace_back([](const std::string& v) { return ARFFValue(std::stod(v)); });
    conversors.emplace_back([](const std::string& v) { return ARFFValue(std::stoi(v)); });
    conversors.emplace_back([](const std::string& v) { return ARFFValue(v); });

    ARFFData data;
    std::string fixture = "Iris,3.4,2,Setosa";
    auto result = data.decode_rows({fixture}, conversors)[0];
    std::vector<ARFFValue> expected = {ARFFValue("Iris"), ARFFValue(3.4), ARFFValue(2), ARFFValue("Setosa")};

    ASSERT_EQ(result.size(), 4);
    EXPECT_EQ(result, expected);
}
// ... [CUT: All other decode/encode tests and error scenarios, matching original logic]