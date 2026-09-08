#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>

// Dummy implementation
std::string get_item_id_by_name(const std::vector<std::map<std::string, std::string>>& list_dict, const std::string& name) {
    for (const auto& item : list_dict) {
        auto itName = item.find("name");
        auto itId = item.find("id");
        if (itName != item.end() && itId != item.end()) {
            if (itName->second == name) return itId->second;
        }
    }
    return "";
}

TEST(TestGetItemIDByName, test_get_item_id_by_name) {
    std::vector<std::map<std::string, std::string>> list_dict{
        {{"name", "channel_name"}, {"id", "123"}},
        { }
    };
    EXPECT_EQ("123", get_item_id_by_name(list_dict, "channel_name"));
}