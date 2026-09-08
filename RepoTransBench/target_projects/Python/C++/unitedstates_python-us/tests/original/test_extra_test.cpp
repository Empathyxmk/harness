#include <gtest/gtest.h>
#include "us.h"

using namespace us;

TEST(StateExtraTest, StateReprAndStr) {
    State &s = AL;
    EXPECT_EQ(s.repr(), "<State:" + s.name + ">");
    EXPECT_EQ(s.str(), s.name);
}

TEST(StateExtraTest, ShapefileUrlsWithFips) {
    State &s = AL;
    auto urls_opt = s.shapefile_urls();
    ASSERT_TRUE(urls_opt.has_value());
    auto urls = urls_opt.value();
    EXPECT_TRUE(urls.find("tract") != urls.end());
    EXPECT_TRUE(urls.find("county") != urls.end());
}

TEST(StateExtraTest, ShapefileUrlsWithoutFips) {
    State s("Fake", "ZZ", std::nullopt, true, true, false, false,
            std::nullopt, std::nullopt, std::nullopt, "FK", std::nullopt, {});
    EXPECT_FALSE(s.shapefile_urls().has_value());
}

TEST(StateExtraTest, LookupWithFieldArgument) {
    const State &md = MD;
    EXPECT_EQ(lookup("MD", "abbr"), &md);
    EXPECT_EQ(lookup("24", "fips"), &md);
    EXPECT_EQ(lookup(md.name_metaphone, "name_metaphone"), &md);
    // Should miss because it's case-sensitive
    EXPECT_EQ(lookup("maryland", "name"), nullptr);
}

TEST(StateExtraTest, LookupNoMatchReturnsNone) {
    EXPECT_EQ(lookup("nonesuchstate"), nullptr);
    EXPECT_EQ(lookup("zzzzzzzzzz"), nullptr);
}

TEST(StateExtraTest, LookupCaching) {
    const char *val = "MD";
    const State *md = lookup(val);
    // Simulate cache: Just re-lookup and expect the same pointer.
    EXPECT_EQ(lookup(val, "", true), md);
}

TEST(StateExtraTest, MappingDefaultAndCustom) {
    auto m = mapping("abbr", "fips", nullptr);
    EXPECT_EQ(m["MD"], "24");
    EXPECT_EQ(m["AL"], "01");

    std::vector<State> vec = {DC, MD};
    auto custom = mapping("abbr", "fips", &vec);
    EXPECT_EQ(custom.size(), 2);
    EXPECT_NE(custom.find("DC"), custom.end());
    EXPECT_NE(custom.find("MD"), custom.end());
}

TEST(StateExtraTest, FIPS_REandABBR_RE) {
    EXPECT_TRUE(FIPS_RE.match("24"));
    EXPECT_FALSE(FIPS_RE.match("a2"));
    EXPECT_TRUE(ABBR_RE.match("MD"));
    EXPECT_TRUE(ABBR_RE.match("md"));
    EXPECT_FALSE(ABBR_RE.match("maryland"));
}

TEST(StateExtraTest, VersionSymbolsValid) {
    EXPECT_FALSE(version.empty());
    EXPECT_EQ(version, "1.0.0");
}

TEST(StateExtraTest, USModuleProperties) {
    EXPECT_EQ(unitedstates_cpp_us::us::version, "1.0.0");
    // We do not test birthday here; module not implemented.
}