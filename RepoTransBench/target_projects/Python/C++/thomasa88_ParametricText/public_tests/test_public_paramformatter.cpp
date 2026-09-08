#include <gtest/gtest.h>
#include "paramformatter.h"

struct PublicParam : public Param {
    PublicParam(double v, std::string u = "") : Param(v, u) {}
};

TEST(PublicParamFormatter, MixedFracInchWholeNumber) {
    PublicParam p(15, "");
    EXPECT_EQ(mixed_frac_inch(p, nullptr), "15\"");
}

TEST(PublicParamFormatter, MixedFracInchSimpleFraction) {
    PublicParam p(0.625, "");
    EXPECT_EQ(mixed_frac_inch(p, nullptr), "5/8\"");
}

TEST(PublicParamFormatter, MixedFracInchMixed) {
    PublicParam p(3.75, "");
    EXPECT_EQ(mixed_frac_inch(p, nullptr), "3 3/4\"");
}

TEST(PublicParamFormatter, MixedFracInchExactHalf) {
    PublicParam p(6.5, "");
    EXPECT_EQ(mixed_frac_inch(p, nullptr), "6 1/2\"");
}

TEST(PublicParamFormatter, MixedFracInchZero) {
    PublicParam p(0, "");
    EXPECT_EQ(mixed_frac_inch(p, nullptr), "0\"");
}