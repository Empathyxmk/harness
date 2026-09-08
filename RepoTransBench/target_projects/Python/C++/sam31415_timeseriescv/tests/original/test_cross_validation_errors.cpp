#include <gtest/gtest.h>
#include <vector>
#include <stdexcept>
#include <string>
#include "cross_validation_stub.h"

struct DummyCV : public BaseTimeSeriesCrossValidator {
    using BaseTimeSeriesCrossValidator::BaseTimeSeriesCrossValidator;
    std::vector<std::pair<std::vector<int>, std::vector<int>>>
    split(const std::vector<std::vector<double>>& X,
          const std::vector<int>* y = nullptr,
          const std::vector<int64_t>* pred_times = nullptr,
          const std::vector<int64_t>* eval_times = nullptr) override {
        return BaseTimeSeriesCrossValidator::split(X, y, pred_times, eval_times);
    }
};

TEST(TestTimeseriescvErrors, NSplitsType) {
    EXPECT_THROW({
        BaseTimeSeriesCrossValidator cv("not_an_int");
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, NSplitsTooLow) {
    EXPECT_THROW({
        BaseTimeSeriesCrossValidator cv(1);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitInvalidXType) {
    DummyCV cv(2);
    EXPECT_THROW({
        cv.split("not_a_dataframe");
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitInvalidYType) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1,2},{3,4}};
    std::vector<int64_t> pred_times = {1,2};
    std::vector<int64_t> eval_times = {1,2};
    EXPECT_THROW({
        cv.split(X, (const std::vector<int>*) &"not_a_series", &pred_times, &eval_times);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitInvalidPredTimesType) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1}};
    std::vector<int> y = {1};
    std::vector<int64_t> eval_times = {1};
    EXPECT_THROW({
        cv.split(X, &y, (const std::vector<int64_t>*) &"not_a_series", &eval_times);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitInvalidEvalTimesType) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1}};
    std::vector<int> y = {1};
    std::vector<int64_t> pred_times = {1};
    EXPECT_THROW({
        cv.split(X, &y, &pred_times, (const std::vector<int64_t>*) &"not_a_series");
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitIndexMismatchY) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1},{2}};
    std::vector<int> y = {1};
    std::vector<int64_t> pred_times = {1,2};
    std::vector<int64_t> eval_times = {1,2};
    EXPECT_THROW({
        cv.split(X, &y, &pred_times, &eval_times);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitIndexMismatchPredTimes) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1},{2}};
    std::vector<int> y = {1,2};
    std::vector<int64_t> pred_times = {3,4};
    std::vector<int64_t> eval_times = {1,2};
    EXPECT_THROW({
        cv.split(X, &y, &pred_times, &eval_times);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitIndexMismatchEvalTimes) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1},{2}};
    std::vector<int> y = {1,2};
    std::vector<int64_t> pred_times = {1,2};
    std::vector<int64_t> eval_times = {99,98};
    EXPECT_THROW({
        cv.split(X, &y, &pred_times, &eval_times);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitPredTimesNotSorted) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1},{2}};
    std::vector<int> y = {1,2};
    std::vector<int64_t> pred_times = {2,1};
    std::vector<int64_t> eval_times = {1,2};
    EXPECT_THROW({
        cv.split(X, &y, &pred_times, &eval_times);
    }, std::invalid_argument);
}

TEST(TestTimeseriescvErrors, SplitEvalTimesNotSorted) {
    DummyCV cv(2);
    std::vector<std::vector<double>> X = {{1},{2}};
    std::vector<int> y = {1,2};
    std::vector<int64_t> pred_times = {1,2};
    std::vector<int64_t> eval_times = {2,1};
    EXPECT_THROW({
        cv.split(X, &y, &pred_times, &eval_times);
    }, std::invalid_argument);
}