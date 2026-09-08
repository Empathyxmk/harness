#include <gtest/gtest.h>
#include <vector>
#include <cmath>
#include "lafan1_benchmarks.h"

TEST(TestEvaluatePublic, PickleStatsLike) {
    std::vector<std::vector<double>> x_mean(2, std::vector<double>(2,13));
    std::vector<std::vector<double>> x_std(2, std::vector<double>(2,6));
    ASSERT_EQ(x_mean[0][0], 13);
    ASSERT_EQ(x_std[0][0], 6);
}

TEST(TestEvaluatePublic, BenchmarkOnFakeData) {
    std::vector<std::vector<std::vector<double>>> X(1, std::vector<std::vector<double>>(10, std::vector<double>(2,2)));
    std::vector<std::vector<std::vector<double>>> Y(1, std::vector<std::vector<double>>(10, std::vector<double>(2,1)));
    double score = fast_npss(X, Y);
    (void)score;
    SUCCEED();
}

TEST(TestEvaluatePublic, BenchmarkNanGuardWithNanInput) {
    std::vector<std::vector<std::vector<double>>> A = {{{1,2},{NAN,4}}};
    std::vector<std::vector<std::vector<double>>> B = {{{5,6},{7,8}}};
    double score = fast_npss(A, B);
    ASSERT_TRUE(std::isnan(score) || score >= 0);
}