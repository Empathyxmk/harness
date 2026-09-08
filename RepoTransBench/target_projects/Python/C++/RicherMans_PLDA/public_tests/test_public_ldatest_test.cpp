#include <gtest/gtest.h>
#include "src/liblda/lda.h"

TEST(TestPublicLDA, FitPublic) {
    std::vector<std::vector<double>> X{{3,8,1},{6,2,7},{5,4,0},{9,1,2}};
    std::vector<int> y{2,2,1,1};
    LDA lda(2);
    LDA& model = lda.fit(X, y);
    ASSERT_EQ(&model, &lda);
    ASSERT_EQ((int)lda.model[0][0], 4); // model[0][0] == n_samples
}

TEST(TestPublicLDA, TransformPublic) {
    std::vector<std::vector<double>> X{{3,8,1},{6,2,7},{5,4,0},{9,1,2}};
    std::vector<int> y{2,2,1,1};
    LDA lda(2);
    lda.fit(X, y);
    std::vector<std::vector<double>> X_new = lda.transform(X);
    ASSERT_EQ((int)X_new[0].size(), 2);
}

TEST(TestPublicLDA, FitTransformPublic) {
    std::vector<std::vector<double>> X{{3,8,1},{6,2,7},{5,4,0},{9,1,2}};
    std::vector<int> y{2,2,1,1};
    LDA lda(2);
    std::vector<std::vector<double>> X_new = lda.fit_transform(X, y);
    ASSERT_EQ((int)X_new[0].size(), 2);
}

TEST(TestPublicLDA, TransformNComponentsNonePublic) {
    std::vector<std::vector<double>> X{{3,8,1},{6,2,7},{5,4,0},{9,1,2}};
    std::vector<int> y{2,2,1,1};
    LDA lda(0); // n_components=None
    lda.fit(X, y);
    std::vector<std::vector<double>> X_new = lda.transform(X);
    ASSERT_EQ(X_new.size(), X.size());
    ASSERT_EQ(X_new[0].size(), X[0].size());
}