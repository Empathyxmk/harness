#include <gtest/gtest.h>
#include "src/liblda/plda.h"

TEST(TestPLDA, Fit) {
    std::vector<std::vector<double>> X{{1,2},{3,4},{5,6}};
    std::vector<int> y{0,1,0};
    PLDA plda;
    PLDA& out = plda.fit(X, y);
    ASSERT_TRUE(plda.trained);
    ASSERT_EQ(&out, &plda);
}

TEST(TestPLDA, Predict) {
    std::vector<std::vector<double>> X{{1,2},{3,4},{5,6}};
    std::vector<int> y{0,1,0};
    PLDA plda;
    plda.fit(X, y);
    std::vector<int> pred = plda.predict(X);
    // pred vector should all be zero
    for (auto v : pred) {
        ASSERT_EQ(v, 0);
    }
}

TEST(TestPLDA, PredictWithoutFit) {
    std::vector<std::vector<double>> X{{1,2},{3,4},{5,6}};
    PLDA p;
    try {
        p.predict(X);
        FAIL() << "Expected std::runtime_error";
    } catch (const std::runtime_error& e) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}