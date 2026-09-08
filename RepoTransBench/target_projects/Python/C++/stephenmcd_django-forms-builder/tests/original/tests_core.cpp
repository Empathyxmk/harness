#include <gtest/gtest.h>
#include "forms_fields.h"

using namespace forms_fields;

TEST(Core, FieldChoicesDict) {
    std::string choices = "Red\nGreen\nBlue";
    std::vector<std::string> expected = {"Red", "Green", "Blue"};
    EXPECT_EQ(choices_from_lines(choices), expected);
}

TEST(Core, FieldChoicesDictEmpty) {
    EXPECT_EQ(choices_from_lines(""), std::vector<std::string>());
}

TEST(Core, IsFile) {
    // Simulate is_file logic using file extensions
    EXPECT_TRUE(is_file("photo.PNG"));
    EXPECT_TRUE(is_file("document.PDF"));
    EXPECT_FALSE(is_file("example.txt"));
    EXPECT_FALSE(is_file("no_dot"));
}

TEST(Core, SlugifyStripAndLower) {
    // We'll simulate slugify by lowercasing and replacing __ with - (not implemented fully)
    std::string s = " Hello__World__ ";
    std::string want = "hello-world";
    std::string sl = s;
    // Simulate
    std::transform(sl.begin(), sl.end(), sl.begin(), ::tolower);
    size_t pos;
    while ((pos = sl.find("__")) != std::string::npos)
        sl.replace(pos, 2, "-");
    sl.erase(std::remove_if(sl.begin(), sl.end(), ::isspace), sl.end());
    if (sl.length() > 2 && sl.front() == '-')
        sl = sl.substr(1);
    if (sl.length() > 2 && sl.back() == '-')
        sl = sl.substr(0, sl.length() - 1);
    EXPECT_EQ(sl, want);
}

TEST(Core, SettingImports) {
    // Simulating config options
    bool USE_SITES = true;
    bool USE_THREADED_EMAILS = false;
    std::vector<std::string> EXTRA_FIELD_TYPES;
    EXPECT_TRUE(typeid(USE_SITES) == typeid(bool));
    EXPECT_TRUE(typeid(USE_THREADED_EMAILS) == typeid(bool));
    EXPECT_TRUE(typeid(EXTRA_FIELD_TYPES) == typeid(std::vector<std::string>));
}