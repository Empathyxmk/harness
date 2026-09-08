#include <gtest/gtest.h>
#include <vector>
#include "lafan1_benchmarks.h"

TEST(TestBenchmarksPublic, FastNPSSSimple) {
    std::vector<std::vector<std::vector<double>>> A(2, std::vector<std::vector<double>>(12, std::vector<double>(1,1.0)));
    std::vector<std::vector<std::vector<double>>> B(2, std::vector<std::vector<double>>(12, std::vector<double>(1,2.0)));
    double score = fast_npss(A, B);
    EXPECT_TRUE(!std::isnan(score));
}

TEST(TestBenchmarksPublic, FastNPSSDifferentNaNGuard) {
    std::vector<std::vector<std::vector<double>>> A(2, std::vector<std::vector<double>>(12, std::vector<double>(1,0.0)));
    std::vector<std::vector<std::vector<double>>> B(2, std::vector<std::vector<double>>(12, std::vector<double>(1,1.0)));
    double score = fast_npss(A, B);
    EXPECT_TRUE(!std::isnan(score));
}