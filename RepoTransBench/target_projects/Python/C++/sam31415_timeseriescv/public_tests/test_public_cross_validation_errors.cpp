#include <gtest/gtest.h>
#include <vector>
#include <stdexcept>
#include <string>
#include "cross_validation_stub.h"

TEST(PublicCrossValidationErrors, ErrorsNSplitsPublic) {
    std::vector<std::vector<double>> df(15, std::vector<double>(1, 0.0));
    EXPECT_THROW({
        PurgedWalkForwardCV(16, 1, 1, 0).split(df).at(0);
    }, std::invalid_argument);
}
TEST(PublicCrossValidationErrors, ErrorsTrainLengthPublic) {
    std::vector<std::vector<double>> df(12, std::vector<double>(1, 0.0));
    EXPECT_THROW({
        PurgedWalkForwardCV(3, 11, 2, 0).split(df).at(0);
    }, std::invalid_argument);
}
TEST(PublicCrossValidationErrors, ErrorsTestLengthPublic) {
    std::vector<std::vector<double>> df(10, std::vector<double>(1, 0.0));
    EXPECT_THROW({
        PurgedWalkForwardCV(2, 2, 9, 0).split(df).at(0);
    }, std::invalid_argument);
}
TEST(PublicCrossValidationErrors, ErrorsLookaheadNegativePublic) {
    EXPECT_THROW({
        PurgedWalkForwardCV(2, 2, 2, -4);
    }, std::invalid_argument);
}
TEST(PublicCrossValidationErrors, BaseCVSplitSignaturePublic) {
    struct DummyCV : public BaseTimeSeriesCrossValidator {
        DummyCV() : BaseTimeSeriesCrossValidator(1) {}
        int get_n_splits(const std::vector<std::vector<double>>* = nullptr, const std::vector<int>* = nullptr,
                         const std::vector<int64_t>* = nullptr, const std::vector<int64_t>* = nullptr) const override {
            return 1;
        }
    };
    std::vector<std::vector<double>> df(4, std::vector<double>(1, 0.0));
    DummyCV dummy;
    EXPECT_THROW({
        dummy.split(df);
    }, std::logic_error);
}