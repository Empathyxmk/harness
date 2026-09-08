#include <gtest/gtest.h>
#include "pythonflow/util.h"

TEST(PublicUtilExtra, MergeDicts) {
    std::map<std::string, int> a = {{"e", 1}, {"f", 2}};
    std::map<std::string, int> b = {{"g", 3}};
    auto m = pythonflow::util::merge_dicts(a, b);
    ASSERT_EQ(m["e"], 1);
    ASSERT_EQ(m["f"], 2);
    ASSERT_EQ(m["g"], 3);
}

// ... (Repeat the rest: test_merge_dicts_conflict, test_find_duplicates, etc)