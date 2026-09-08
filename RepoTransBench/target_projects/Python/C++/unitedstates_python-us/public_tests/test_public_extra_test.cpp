#include <gtest/gtest.h>
#include "us.h"
#include <set>

using namespace us;

TEST(PublicExtraTest, StateNameAndAbbr) {
    EXPECT_EQ(CA.name, "California");
    EXPECT_EQ(NY.abbr, "NY");
}

TEST(PublicExtraTest, StateAlternate) {
    EXPECT_EQ(NY.fips, std::make_optional<std::string>("36"));
    EXPECT_EQ(NV.capital, std::make_optional<std::string>("Carson City"));
}

TEST(PublicExtraTest, StateNumeric) {
    State &tx = TX;
    ASSERT_TRUE(tx.fips.has_value());
    EXPECT_TRUE(!tx.fips->empty());
    EXPECT_TRUE(std::all_of(tx.fips->begin(), tx.fips->end(), ::isdigit));
}

TEST(PublicExtraTest, ContinentalStatesExcludesDC) {
    std::set<std::string> abbrs;
    for (const auto &st : STATES)
        abbrs.insert(st.abbr);
    EXPECT_TRUE(abbrs.find("DC") == abbrs.end());
    EXPECT_TRUE(abbrs.find("CA") != abbrs.end());
    EXPECT_TRUE(abbrs.find("NY") != abbrs.end());
}

TEST(PublicExtraTest, StatesObjectIsIterableAndLen) {
    std::set<std::string> all_names;
    for (const auto &st : STATES)
        all_names.insert(st.name);
    EXPECT_TRUE(all_names.find("Wyoming") != all_names.end());
    std::set<std::string> us_state_abbrs;
    for (const auto &st : STATES)
        if (st.abbr != "DC" && st.abbr != "AS" && st.abbr != "GU" && st.abbr != "MP" && st.abbr != "PR" && st.abbr != "VI")
            us_state_abbrs.insert(st.abbr);
    EXPECT_EQ(us_state_abbrs.size(), 13); // Our sample has 13 states
}

TEST(PublicExtraTest, FieldTypes) {
    State &tx = TX;
    EXPECT_TRUE(tx.capital.has_value());
    EXPECT_FALSE(tx.capital->empty());
    EXPECT_GE(tx.time_zones.size(), 1U);
}

TEST(PublicExtraTest, ListMembershipAndEquality) {
    const State &ca = CA;
    bool found = false;
    for (const auto &st : STATES) {
        if (st.name == "California") {
            found = true;
            EXPECT_EQ(st, ca);
        }
    }
    EXPECT_TRUE(found);
}

TEST(PublicExtraTest, AllStatesHaveFipsAndNames) {
    for (const auto &st : STATES) {
        EXPECT_TRUE(st.fips.has_value());
        EXPECT_FALSE(st.name.empty());
    }
}

TEST(PublicExtraTest, NonTypicalStateFIPS) {
    State &pr = PR;
    EXPECT_EQ(pr.fips, std::make_optional<std::string>("72"));
    EXPECT_EQ(pr.name, "Puerto Rico");
}

TEST(PublicExtraTest, StateProperties) {
    const State &arizona = AZ;
    EXPECT_EQ(arizona.capital, std::make_optional<std::string>("Phoenix"));
    bool has_america_tz = false;
    for (const auto &tz : arizona.time_zones) {
        if (tz.find("America/") != std::string::npos)
            has_america_tz = true;
    }
    EXPECT_TRUE(has_america_tz);
}