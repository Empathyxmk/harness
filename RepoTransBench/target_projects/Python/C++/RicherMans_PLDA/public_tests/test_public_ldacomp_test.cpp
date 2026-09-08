#include <gtest/gtest.h>
#include "src/liblda/lda.h"

TEST(TestPublicLDAComp, LDAFitAndTransformPublic) {
    std::vector<std::vector<double>> X{{2,6,4},{1,5,8},{4,2,9}};
    std::vector<int> y{1,0,0};
    LDA lda(2);
    lda.fit(X, y);
    std::vector<std::vector<double>> X_trans = lda.transform(X);
    ASSERT_EQ((int)X_trans.size(), 3);
    ASSERT_EQ((int)X_trans[0].size(), 2);
}