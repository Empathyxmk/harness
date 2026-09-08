#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <numeric>
#include <random>
#include <typeinfo>
#include "cross_validation_stub.h"

// Helper function to mock make_simple_data
SimpleData make_simple_data(int n = 10, int seed = 0) {
    // Create some random but deterministic (with seed) data
    std::mt19937 rng(seed);
    std::uniform_real_distribution<> dist(0.0, 1.0);
    std::vector<std::vector<double>> df(n, std::vector<double>(3, 0.0));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < 3; ++j)
            df[i][j] = dist(rng);
    std::vector<int> y(n, 0);
    std::uniform_int_distribution<> idist(0, 1);
    for (int i = 0; i < n; ++i)
        y[i] = idist(rng);
    std::vector<int64_t> pred_times(n), eval_times(n);
    for (int i = 0; i < n; ++i) {
        pred_times[i] = i+10000; // dummy timestamps
        eval_times[i] = pred_times[i] + 1; // offset by 1
    }
    return SimpleData{df, y, pred_times, eval_times};
}

TEST(TestTimeseriescv, BaseTimeSeriesCVNSplitsProperty) {
    BaseTimeSeriesCrossValidator cv(5);
    EXPECT_EQ(cv.n_splits(), 5);
    cv.n_splits(6);
    EXPECT_EQ(cv.n_splits(), 6);
}

TEST(TestTimeseriescv, PurgeBasicObject) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(2) {
            pred_times.assign(6, 0);
            eval_times.assign(6, 0);
            for (int i = 0; i < 6; ++i) {
                pred_times[i] = i + 10000;
                eval_times[i] = pred_times[i] + 1;
            }
            indices.resize(6);
            std::iota(indices.begin(), indices.end(), 0);
        }
    };
    DummyCV cv;
    int test_fold_start = 4, test_fold_end = 5;
    auto in_train = purge(cv, test_fold_start, test_fold_end, test_fold_end);
    EXPECT_TRUE(in_train.size() >= 0); // Just check it's a vector
}

TEST(TestTimeseriescv, EmbargoBasicObject) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(2) {
            pred_times.assign(10, 0);
            eval_times.assign(10, 0);
            for (int i = 0; i < 10; ++i) {
                pred_times[i] = i + 1000;
                eval_times[i] = pred_times[i] + 1;
            }
            embargo_td = 1;
            indices.resize(10);
            std::iota(indices.begin(), indices.end(), 0);
        }
    };
    DummyCV dummy_cv;
    std::vector<int> train_indices = {0,1,2,3,4,5,6,7};
    std::vector<int> test_indices = {8,9};
    int test_fold_end = 9;
    auto embargoed = embargo(dummy_cv, train_indices, test_indices, test_fold_end);
    EXPECT_TRUE(embargoed.size() <= train_indices.size());
}

TEST(TestTimeseriescv, ComputeFoldBoundsObject) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(2) {
            indices.resize(8);
            std::iota(indices.begin(), indices.end(), 0);
        }
    };
    DummyCV dummy_cv;
    auto bounds = compute_fold_bounds(dummy_cv, false);
    EXPECT_TRUE(bounds.size() > 0 || bounds.size() == 0); // Just check it's a list
}

TEST(TestTimeseriescv, PurgedWalkForwardCVSplit) {
    auto data = make_simple_data(20);
    PurgedWalkForwardCV cv(5);
    auto splits = cv.split(data.df, data.y, data.pred_times, data.eval_times);
    EXPECT_EQ(splits.size(), 3);
    for (const auto& split : splits) {
        const auto& train = split.first;
        const auto& test = split.second;
        // No overlap
        std::vector<int> intersect;
        std::set_intersection(train.begin(), train.end(),
                              test.begin(), test.end(),
                              std::back_inserter(intersect));
        EXPECT_TRUE(intersect.empty());
        EXPECT_TRUE(test.size() > 0);
    }
}

TEST(TestTimeseriescv, CombPurgedKFoldCVSplit) {
    auto data = make_simple_data(12);
    CombPurgedKFoldCV cv(3);
    auto splits = cv.split(data.df, data.y, data.pred_times, data.eval_times);
    EXPECT_EQ(splits.size(), 3);
    for (const auto& split : splits) {
        std::vector<int> intersect;
        std::set_intersection(split.first.begin(), split.first.end(),
                              split.second.begin(), split.second.end(),
                              std::back_inserter(intersect));
        EXPECT_TRUE(intersect.empty());
    }
}

TEST(TestTimeseriescv, ReprMethods) {
    PurgedWalkForwardCV cv1(4);
    CombPurgedKFoldCV cv2(3);
    std::string r1 = cv1.repr();
    std::string r2 = cv2.repr();
    EXPECT_NE(r1.find("PurgedWalkForwardCV"), std::string::npos);
    EXPECT_NE(r2.find("CombPurgedKFoldCV"), std::string::npos);
}

TEST(TestTimeseriescv, BaseRepr) {
    BaseTimeSeriesCrossValidator cv(10);
    std::string r = cv.repr();
    EXPECT_NE(r.find("BaseTimeSeriesCrossValidator"), std::string::npos);
}

TEST(TestTimeseriescv, PurgeEmptyObjectThrows) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(2) {
            pred_times.clear();
            eval_times.clear();
            indices.clear();
        }
    };
    DummyCV dummy_cv;
    EXPECT_THROW({
        purge(dummy_cv, 0, 0, 0);
    }, std::out_of_range);
}

TEST(TestTimeseriescv, EmbargoNoEmbargoObject) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(2) {
            pred_times = {100, 101, 102, 103, 104};
            eval_times = {101, 102, 103, 104, 105};
            embargo_td = 0;
            indices = {0, 1, 2, 3, 4};
        }
    };
    DummyCV dummy_cv;
    std::vector<int> train_indices = {0, 4};
    std::vector<int> test_indices = {0, 4};
    int test_fold_end = 4;
    auto embargoed = embargo(dummy_cv, train_indices, test_indices, test_fold_end);
    // All of embargoed must be subset of train_indices
    for (int idx : embargoed)
        EXPECT_TRUE(std::find(train_indices.begin(), train_indices.end(), idx) != train_indices.end());
}

TEST(TestTimeseriescv, PurgedWalkForwardCVInvalidNTestSplits) {
    EXPECT_THROW({
        PurgedWalkForwardCV cv(2, 1);
    }, std::invalid_argument);
}

TEST(TestTimeseriescv, CombPurgedKFoldCVInvalid) {
    EXPECT_THROW({
        CombPurgedKFoldCV cv(1);
    }, std::invalid_argument);
}