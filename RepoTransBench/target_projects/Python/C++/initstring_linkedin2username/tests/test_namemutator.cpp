#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <set>
#include "linkedin2username.h"

// Helper for equality of std::map<std::string, std::string>
template<typename K, typename V>
::testing::AssertionResult MapEQ(const std::map<K, V>& lhs, const std::map<K, V>& rhs) {
    if (lhs.size() != rhs.size()) {
        return ::testing::AssertionFailure() << "size mismatch: lhs has " << lhs.size() << " keys, rhs has " << rhs.size();
    }
    for (const auto& kv : lhs) {
        auto it = rhs.find(kv.first);
        if (it == rhs.end()) {
            return ::testing::AssertionFailure() << "rhs missing key: " << kv.first;
        }
        if (it->second != kv.second) {
            return ::testing::AssertionFailure() << "value mismatch at key " << kv.first << ": lhs=" << kv.second << ", rhs=" << it->second;
        }
    }
    return ::testing::AssertionSuccess();
}

// Parametrize TABLE for NameMutator.name result
struct NameCase {
    std::string input_name;
    std::map<std::string, std::string> expected;
};

class NameMutatorCleanAndSplitTest : public ::testing::TestWithParam<NameCase> {};

TEST_P(NameMutatorCleanAndSplitTest, CleanAndSplit) {
    auto param = GetParam();
    NameMutator nm(param.input_name);
    EXPECT_TRUE(MapEQ(nm.name, param.expected));
}

INSTANTIATE_TEST_SUITE_P(
    NameMutatorTests, NameMutatorCleanAndSplitTest,
    ::testing::Values(
        NameCase{"John Smith", {{"first", "john"}, {"second", "smith"}}},
        NameCase{"Jane D'oe", {{"first", "jane"}, {"second", "doe"}}},
        NameCase{"Dr. Ángela Gómez (MBA, PhD)", {{"first", "angela"}, {"second", "gomez"}}},
        NameCase{"Mr. François Noël", {{"first", "francois"}, {"second", "noel"}}},
        NameCase{"José Niño", {{"first", "jose"}, {"second", "nino"}}},
        NameCase{"Joe (CTO) Bloggs", {{"first", "joe"}, {"second", "bloggs"}}},
        NameCase{"Alíce O'Conñor (CISO)", {{"first", "alice"}, {"second", "oconor"}}},
        NameCase{"Mononym", {{"first", "mononym"}, {"second", ""}}}
    )
);

// Parametrize TABLE for NameMutator.first()
struct NameToFirst {
    std::string input_name;
    std::string expected;
};

class NameMutatorFirstTest : public ::testing::TestWithParam<NameToFirst> {};

TEST_P(NameMutatorFirstTest, First) {
    auto param = GetParam();
    NameMutator nm(param.input_name);
    auto s = nm.first();
    if (s.empty())
        EXPECT_EQ(param.expected, "");
    else
        EXPECT_TRUE(s.count(param.expected));
}

INSTANTIATE_TEST_SUITE_P(
    NameMutatorTests, NameMutatorFirstTest,
    ::testing::Values(
        NameToFirst{"John Smith", "john"},
        NameToFirst{" Jane Smith ", "jane"},
        NameToFirst{"Dr. Ángela Gómez (MBA, PhD)", "angela"},
        NameToFirst{"Mononym", "mononym"},
        NameToFirst{"", ""}
    )
);

// Parametrize TABLE for NameMutator.last()
struct NameToLast {
    std::string input_name;
    std::string expected;
};

class NameMutatorLastTest : public ::testing::TestWithParam<NameToLast> {};

TEST_P(NameMutatorLastTest, Last) {
    auto param = GetParam();
    NameMutator nm(param.input_name);
    auto s = nm.last();
    if (s.empty())
        EXPECT_EQ(param.expected, "");
    else
        EXPECT_TRUE(s.count(param.expected));
}

INSTANTIATE_TEST_SUITE_P(
    NameMutatorTests, NameMutatorLastTest,
    ::testing::Values(
        NameToLast{"John Smith", "smith"},
        NameToLast{"Jane D'oe", "doe"},
        NameToLast{"Dr. Ángela Gómez (MBA, PhD)", "gomez"},
        NameToLast{"Mr. François Noël", "noel"},
        NameToLast{"José Niño", "nino"},
        NameToLast{"Joe (CTO) Bloggs", "bloggs"},
        NameToLast{"Alíce O'Conñor (CISO)", "oconor"},
        NameToLast{"Mononym", ""},
        NameToLast{"", ""}
    )
);

TEST(NameMutatorFull, MutatorsAllVariants) {
    NameMutator nm("John O'Conner (CEO)");
    std::set<std::string> variants(nm.mutators().begin(), nm.mutators().end());
    EXPECT_TRUE(variants.count("johnoconner") > 0);
    EXPECT_TRUE(variants.count("joconner") > 0);

    bool has_john_o = false, has_johno = false;
    for (const auto& v : variants) {
        if (v.find("john.o") != std::string::npos) has_john_o = true;
        if (v.find("johno") != std::string::npos) has_johno = true;
    }
    EXPECT_TRUE(has_john_o || has_johno);
}

TEST(NameMutatorFull, NameWithEmptyString) {
    NameMutator nm("");
    EXPECT_TRUE(MapEQ(nm.name, {{"first", ""}, {"second", ""}}));
    EXPECT_TRUE(nm.mutators().empty());
}