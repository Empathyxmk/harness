#include <gtest/gtest.h>
#include <vector>
#include <stdexcept>
#include <numeric>
#include <algorithm>
#include <set>
#include "cross_validation_stub.h"

TEST(PublicCrossValidation, PurgedWalkForwardCVNonDefault) {
    std::vector<std::vector<double>> df(30, std::vector<double>(1, 0.0));
    for (int i = 0; i < 30; ++i)
        df[i][0] = i + 40; // value: 40..69
    PurgedWalkForwardCV cv(5, 6, 2, 1);
    auto splits = cv.split(df);
    ASSERT_EQ(splits.size(), 5);
    EXPECT_EQ(splits.front().first.front(), 0);
    EXPECT_EQ(splits.back().second.back(), static_cast<int>(df.size())-1);
}

TEST(PublicCrossValidation, EmbargoPublic) {
    std::vector<bool> arr(20, false);
    embargo(arr, 6, 13, 4);
    // 13,14,15,16 should be embargoed
    for (int i = 13; i <= 16; ++i)
        EXPECT_TRUE(arr[i]);
    EXPECT_FALSE(arr[12]);
}

TEST(PublicCrossValidation, WalkForwardLengthPublic) {
    std::vector<std::vector<double>> X(34, std::vector<double>(1, 0.0));
    for (int i = 0; i < 34; ++i) X[i][0] = i + 30;
    PurgedWalkForwardCV cv(2, 12, 9, 2);
    auto splits = cv.split(X);
    ASSERT_EQ(splits.size(), 2);
    int last = -1;
    for (const auto &split : splits) {
        EXPECT_GT(split.second[0], last);
        last = split.second.back();
    }
}

TEST(PublicCrossValidation, ReprPublic) {
    PurgedWalkForwardCV cv(3, 8, 3, 3);
    std::string rp = cv.repr();
    EXPECT_NE(rp.find("PurgedWalkForwardCV"), std::string::npos);
    EXPECT_NE(rp.find("n_splits=3"), std::string::npos);
}

TEST(PublicCrossValidation, CrossValidatorBasePublic) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(1) {}
        std::vector<std::pair<std::vector<int>, std::vector<int>>>
        split(const std::vector<std::vector<double>>& X,
              const std::vector<int>* y = nullptr,
              const std::vector<int64_t>* pred_times = nullptr,
              const std::vector<int64_t>* eval_times = nullptr) override {
            int n = X.size();
            return { { std::vector<int>(n/3), std::vector<int>(n/2-n/3) } };
        }
        int get_n_splits(const std::vector<std::vector<double>>* = nullptr, const std::vector<int>* = nullptr,
                         const std::vector<int64_t>* = nullptr, const std::vector<int64_t>* = nullptr) const override {
            return 1;
        }
    };
    std::vector<std::vector<double>> X(10, std::vector<double>(1, 0.0));
    auto splits = DummyCV().split(X);
    ASSERT_EQ(splits.size(), 1);
    const auto& train_idx = splits[0].first;
    const auto& test_idx = splits[0].second;
    EXPECT_GE(train_idx.size(), 0);
    EXPECT_GE(test_idx.size(), 0);
    std::set<int> train_set(train_idx.begin(), train_idx.end());
    std::set<int> test_set(test_idx.begin(), test_idx.end());
    for (int idx : train_set) EXPECT_TRUE(test_set.find(idx) == test_set.end());
}

TEST(PublicCrossValidation, PurgedWalkForwardCVGetNSplitsPublic) {
    std::vector<std::vector<double>> df(29, std::vector<double>(1, 0.0));
    for (int i = 0; i < 29; ++i) df[i][0] = 30+i;
    PurgedWalkForwardCV cv(3, 7, 2, 2);
    EXPECT_EQ(cv.get_n_splits(df), 3);
}

TEST(PublicCrossValidation, SplitIndicesNonOverlapPublic) {
    std::vector<std::vector<double>> df(24, std::vector<double>(1, 0.0));
    for (int i = 0; i < 24; ++i) df[i][0]=70+i;
    PurgedWalkForwardCV cv(4, 5, 5, 3);
    auto splits = cv.split(df);
    for (const auto& split : splits) {
        std::set<int> tr(split.first.begin(), split.first.end());
        for (int idx : split.second) EXPECT_TRUE(tr.find(idx) == tr.end());
    }
}

TEST(PublicCrossValidation, LargeEmbargoEdgePublic) {
    std::vector<bool> mask(12, false);
    embargo(mask, 8, 10, 4);
    for (int i = 10; i < 12; ++i)
        EXPECT_TRUE(mask[i]);
}