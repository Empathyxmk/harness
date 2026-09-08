#include <gtest/gtest.h>
#include "src/liblda/lda.h"

TEST(TestLDA, Fit) {
    std::vector<std::vector<double>> X{{1,2,3},{4,5,6},{7,8,9},{2,3,4}};
    std::vector<int> y{0,1,0,1};
    LDA lda(2);
    LDA& model = lda.fit(X, y);
    ASSERT_EQ(&model, &lda);
    ASSERT_EQ((int)lda.model[0][0], 4); // n_samples
}

TEST(TestLDA, Transform) {
    std::vector<std::vector<double>> X{{1,2,3},{4,5,6},{7,8,9},{2,3,4}};
    std::vector<int> y{0,1,0,1};
    LDA lda(2);
    lda.fit(X, y);
    std::vector<std::vector<double>> X_new = lda.transform(X);
    ASSERT_EQ((int)X_new[0].size(), 2);
}

TEST(TestLDA, FitTransform) {
    std::vector<std::vector<double>> X{{1,2,3},{4,5,6},{7,8,9},{2,3,4}};
    std::vector<int> y{0,1,0,1};
    LDA lda(2);
    std::vector<std::vector<double>> X_new = lda.fit_transform(X, y);
    ASSERT_EQ((int)X_new[0].size(), 2);
}

TEST(TestLDA, TransformNComponentsNone) {
    std::vector<std::vector<double>> X{{1,2,3},{4,5,6},{7,8,9},{2,3,4}};
    std::vector<int> y{0,1,0,1};
    LDA lda(0); // n_components=None
    lda.fit(X, y);
    std::vector<std::vector<double>> X_new = lda.transform(X);
    ASSERT_EQ(X_new.size(), X.size());
    ASSERT_EQ(X_new[0].size(), X[0].size());
}