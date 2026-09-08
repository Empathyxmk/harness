#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <unordered_map>

TEST(TestPublicAdditional, test_truth_public) {
    std::string s = "nonempty";
    EXPECT_TRUE(!s.empty());
}

TEST(TestPublicAdditional, test_split_string_public) {
    std::string s = "foo bar baz";
    std::vector<std::string> parts;
    size_t pos = 0, found;
    while((found = s.find(' ', pos)) != std::string::npos){
        parts.push_back(s.substr(pos, found - pos));
        pos = found + 1;
    }
    parts.push_back(s.substr(pos));
    ASSERT_EQ(parts.size(), 3);
    EXPECT_EQ(parts[0], "foo");
    EXPECT_EQ(parts[1], "bar");
    EXPECT_EQ(parts[2], "baz");
}

TEST(TestPublicAdditional, test_sorted_list_public) {
    std::vector<int> lst = {10, 2, 4, 8};
    std::sort(lst.begin(), lst.end());
    std::vector<int> expected = {2, 4, 8, 10};
    EXPECT_EQ(lst, expected);
}

TEST(TestPublicAdditional, test_dict_access_public) {
    std::unordered_map<std::string, int> d;
    d["alpha"] = 1;
    d["beta"] = 2;
    EXPECT_EQ(d["beta"], 2);
    EXPECT_TRUE(d.count("alpha") == 1);
}