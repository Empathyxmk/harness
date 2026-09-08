#include <gtest/gtest.h>
#include "paramparser.h"

TEST(ParamParseTest, SplitParam) {
    EXPECT_EQ(*ParamSpec::from_string("_"), ParamSpec("_"));
    EXPECT_EQ(*ParamSpec::from_string("_.version"), ParamSpec("_", std::string("version")));
    EXPECT_EQ(*ParamSpec::from_string("_.version:02d"), ParamSpec("_", std::string("version"), std::nullopt, std::string("02d")));
    EXPECT_EQ(*ParamSpec::from_string("_.file[1:5]"), ParamSpec("_", std::string("file"), std::make_pair(1,5)));
    EXPECT_EQ(*ParamSpec::from_string("_.file[1:5]:01"), ParamSpec("_", std::string("file"), std::make_pair(1,5), std::string("01")));
    EXPECT_EQ(*ParamSpec::from_string("param"), ParamSpec("param"));
    EXPECT_EQ(*ParamSpec::from_string("param:-<2"), ParamSpec("param", std::nullopt, std::nullopt, std::string("-<2")));
    EXPECT_EQ(*ParamSpec::from_string("param[1]:-<2"), ParamSpec("param", std::nullopt, std::make_pair(1,2), std::string("-<2")));
    EXPECT_EQ(*ParamSpec::from_string("param[-1:]"), ParamSpec("param", std::nullopt, std::make_pair(-1,99999)));
    EXPECT_EQ(*ParamSpec::from_string("param[:-3]"), ParamSpec("param", std::nullopt, std::make_pair(-99999,-3)));
}

TEST(ParamParseTest, SliceParsing) {
    EXPECT_EQ(*ParamSpec::from_string("p[0]"), ParamSpec("p", std::nullopt, std::make_pair(0,1)));
    EXPECT_EQ(*ParamSpec::from_string("p[:5]"), ParamSpec("p", std::nullopt, std::make_pair(-99999,5)));
    EXPECT_EQ(*ParamSpec::from_string("p[6:]"), ParamSpec("p", std::nullopt, std::make_pair(6,99999)));
    EXPECT_EQ(*ParamSpec::from_string("p[5:6]"), ParamSpec("p", std::nullopt, std::make_pair(5,6)));
    EXPECT_EQ(*ParamSpec::from_string("p[:-1]"), ParamSpec("p", std::nullopt, std::make_pair(-99999,-1)));
    EXPECT_EQ(*ParamSpec::from_string("p[1:-2]"), ParamSpec("p", std::nullopt, std::make_pair(1,-2)));

    EXPECT_EQ(*ParamSpec::from_string("p[:]"), ParamSpec("p", std::nullopt, std::make_pair(-99999,99999)));
    EXPECT_EQ(*ParamSpec::from_string("p[-5:5]"), ParamSpec("p", std::nullopt, std::make_pair(-5,5)));
    EXPECT_EQ(*ParamSpec::from_string("p[11:5]"), ParamSpec("p", std::nullopt, std::make_pair(11,5)));

    EXPECT_FALSE(ParamSpec::from_string("p[]").has_value());
    EXPECT_FALSE(ParamSpec::from_string("p[a]").has_value());
    EXPECT_FALSE(ParamSpec::from_string("p[a:b]").has_value());
    EXPECT_FALSE(ParamSpec::from_string("p[:b]").has_value());
    EXPECT_FALSE(ParamSpec::from_string("p[1:3:2]").has_value());
    EXPECT_FALSE(ParamSpec::from_string("p[::]").has_value());
}

TEST(ParamParseTest, SplitExampleStrings) {
    EXPECT_EQ(*ParamSpec::from_string("d1:.3f"), ParamSpec("d1", std::nullopt, std::nullopt, std::string(".3f")));
    EXPECT_EQ(*ParamSpec::from_string("d1.unit"), ParamSpec("d1", std::string("unit")));
    EXPECT_EQ(*ParamSpec::from_string("d1:03.0f"), ParamSpec("d1", std::nullopt, std::nullopt, std::string("03.0f")));
    EXPECT_EQ(*ParamSpec::from_string("width:.0f"), ParamSpec("width", std::nullopt, std::nullopt, std::string(".0f")));
    EXPECT_EQ(*ParamSpec::from_string("width.expr"), ParamSpec("width", std::string("expr")));
    EXPECT_EQ(*ParamSpec::from_string("height.expr"), ParamSpec("height", std::string("expr")));
    EXPECT_EQ(*ParamSpec::from_string("_.version"), ParamSpec("_", std::string("version")));
    EXPECT_EQ(*ParamSpec::from_string("_.version:03"), ParamSpec("_", std::string("version"), std::nullopt, std::string("03")));
    EXPECT_EQ(*ParamSpec::from_string("_.file"), ParamSpec("_", std::string("file")));
    EXPECT_EQ(*ParamSpec::from_string("_.component"), ParamSpec("_", std::string("component")));
    EXPECT_EQ(*ParamSpec::from_string("_.date"), ParamSpec("_", std::string("date")));
    EXPECT_EQ(*ParamSpec::from_string("_.date:%m/%d/%Y"), ParamSpec("_", std::string("date"), std::nullopt, std::string("%m/%d/%Y")));
    EXPECT_EQ(*ParamSpec::from_string("_.date:%U"), ParamSpec("_", std::string("date"), std::nullopt, std::string("%U")));
    EXPECT_EQ(*ParamSpec::from_string("_.date:%W"), ParamSpec("_", std::string("date"), std::nullopt, std::string("%W")));
    EXPECT_EQ(*ParamSpec::from_string("_.date:%H:%M"), ParamSpec("_", std::string("date"), std::nullopt, std::string("%H:%M")));
}

TEST(ParamParseTest, BadParamString) {
    std::vector<std::string> bad_strings = {
        "",
        ".",
        ".a",
        "a.",
        ".a[10]",
        ".a:5",
        ".[]",
        "a[]",
        "[]",
        ":",
        "a[",
        "a]",
        "[1]",
        "a[1",
        ":5",
        "a[10:10][]"
    };
    for (auto& bad : bad_strings) {
        EXPECT_FALSE(ParamSpec::from_string(bad).has_value()) << "Input: " << bad;
    }
}