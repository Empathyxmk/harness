#include <gtest/gtest.h>
#include "us.h"

using namespace us;

// Helper for lookups in tests
const State* must_lookup(const std::string &s) {
    const State* st = lookup(s);
    EXPECT_NE(st, nullptr);
    return st;
}

TEST(StateUsTest, Attribute) {
    for (const auto &state : STATES_AND_TERRITORIES) {
        const State *state2 = lookup(state.abbr, "abbr");
        ASSERT_NE(state2, nullptr);
        EXPECT_EQ(state.abbr, state2->abbr);
        EXPECT_EQ(state.fips, state2->fips);
        EXPECT_EQ(state.name, state2->name);
        EXPECT_FALSE(state.str().empty());
        EXPECT_FALSE(state.repr().empty());
    }
}

TEST(StateUsTest, FipsLookup) {
    EXPECT_EQ(lookup("24")->abbr, MD.abbr);
    EXPECT_NE(lookup("51")->abbr, MD.abbr);
}

TEST(StateUsTest, AbbrLookup) {
    EXPECT_EQ(lookup("MD")->abbr, MD.abbr);
    EXPECT_EQ(lookup("md")->abbr, MD.abbr);
    EXPECT_NE(lookup("VA")->abbr, MD.abbr);
    EXPECT_NE(lookup("va")->abbr, MD.abbr);
}

TEST(StateUsTest, NameLookup) {
    EXPECT_EQ(lookup("Maryland")->abbr, MD.abbr);
    EXPECT_EQ(lookup("maryland")->abbr, MD.abbr);
    EXPECT_EQ(lookup("Maryland", "name")->abbr, MD.abbr);
    EXPECT_EQ(lookup("maryland", "name"), nullptr);
    EXPECT_EQ(lookup("murryland")->abbr, MD.abbr);
    EXPECT_NE(lookup("Virginia")->abbr, MD.abbr);
}

TEST(StateUsTest, AbbrLookupAllStates) {
    for (const auto& state : STATES) {
        const State* found = lookup(state.abbr);
        ASSERT_NE(found, nullptr);
        EXPECT_EQ(found->abbr, state.abbr);
        EXPECT_EQ(found->name, state.name);
    }
}

TEST(StateUsTest, FipsLookupAllStates) {
    for (const auto& state : STATES) {
        const State* found = lookup(state.fips.value());
        ASSERT_NE(found, nullptr);
        EXPECT_EQ(found->abbr, state.abbr);
        EXPECT_EQ(found->name, state.name);
    }
}

TEST(StateUsTest, NameLookupAllStates) {
    for (const auto& state : STATES) {
        const State* found = lookup(state.name);
        ASSERT_NE(found, nullptr);
        EXPECT_EQ(found->abbr, state.abbr);
        EXPECT_EQ(found->name, state.name);
    }
}

TEST(StateUsTest, ObsoleteLookup) {
    for (const auto& state : OBSOLETE) {
        EXPECT_EQ(lookup(state.name), nullptr);
    }
}

TEST(StateUsTest, JellyfishMetaphone) {
    for (const auto& state : STATES_AND_TERRITORIES) {
        EXPECT_EQ(state.name_metaphone, metaphone(state.name));
    }
    for (const auto& state : OBSOLETE) {
        EXPECT_EQ(state.name_metaphone, metaphone(state.name));
    }
}

TEST(StateUsTest, Mapping) {
    std::vector<State> states5(STATES.begin(), STATES.begin() + std::min(size_t(5), STATES.size()));
    auto m = mapping("abbr", "fips", &states5);
    std::map<std::string, std::string> expected;
    for (const auto &s : states5) {
        expected[s.abbr] = s.fips.value();
    }
    EXPECT_EQ(m, expected);
}

TEST(StateUsTest, ObsoleteMapping) {
    auto m = mapping("abbr", "fips", nullptr);
    for (const auto &state : OBSOLETE) {
        EXPECT_EQ(m.find(state.abbr), m.end());
    }
}

TEST(StateUsTest, CustomMapping) {
    std::vector<State> custom = {DC, MD};
    auto m = mapping("abbr", "fips", &custom);
    EXPECT_EQ(m.size(), 2);
    EXPECT_NE(m.find("DC"), m.end());
    EXPECT_NE(m.find("MD"), m.end());
}

TEST(StateUsTest, KentuckyUppercase) {
    EXPECT_EQ(lookup("kentucky")->abbr, KY.abbr);
    EXPECT_EQ(lookup("KENTUCKY")->abbr, KY.abbr);
}

TEST(StateUsTest, WayomingEdgeCase) {
    EXPECT_EQ(lookup("Wyoming")->abbr, WY.abbr);
    EXPECT_EQ(lookup("Wayoming"), nullptr);
}

TEST(StateUsTest, DCNotState) {
    auto it = std::find(STATES.begin(), STATES.end(), DC);
    EXPECT_EQ(it, STATES.end());
}

TEST(StateUsTest, ObsoleteCount) {
    EXPECT_EQ(OBSOLETE.size(), 0);
}

TEST(StateUsTest, StatesCount) {
    EXPECT_EQ(STATES.size(), 13);
}

TEST(StateUsTest, TerritoriesCount) {
    EXPECT_EQ(TERRITORIES.size(), 2);
}

TEST(StateUsTest, ContiguousCount) {
    EXPECT_EQ(STATES_CONTIGUOUS.size(), 12);
}

TEST(StateUsTest, ContinentalCount) {
    EXPECT_EQ(STATES_CONTINENTAL.size(), 12);
}