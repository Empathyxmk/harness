#include <gtest/gtest.h>

TEST(PublicDjangoFields, SkipDjangoField1) {
    GTEST_SKIP() << "Django fields not tested in public variant.";
}

TEST(PublicDjangoFields, SkipDjangoField2) {
    GTEST_SKIP() << "Django fields not tested in public variant.";
}