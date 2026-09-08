#include <gtest/gtest.h>

TEST(Django, SkipDueToMissingIpware) {
    GTEST_SKIP() << "Skipping due to missing ipware dependency required by pytracking.django.";
}