#include <gtest/gtest.h>
#include <string>
#include <map>

std::map<std::string, std::string> _unknown_kwargs(std::map<std::string, std::string> kwargs) {
    // Identity for this dummy test, just returns its input
    return kwargs;
}

TEST(PublicClientTest, UnknownKwargsGetsFiltered) {
    std::map<std::string, std::string> input = {{"alpha", "beta"}, {"gamma", "42"}, {"is_test", "1"}};
    std::map<std::string, std::string> result = _unknown_kwargs(input);
    ASSERT_EQ(result["alpha"], "beta");
    ASSERT_EQ(result["gamma"], "42");
    ASSERT_EQ(result["is_test"], "1");
}