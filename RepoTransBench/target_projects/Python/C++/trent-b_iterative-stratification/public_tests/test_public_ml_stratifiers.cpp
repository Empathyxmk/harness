#include <gtest/gtest.h>
#include <vector>
#include <algorithm>
#include <memory>
#include <random>
#include "iterative_stratification.hpp"

// Helper types
using MatrixInt = std::vector<std::vector<int>>;
using VectorDouble = std::vector<double>;

class PublicDummyRandomState : public DummyRandomState {
public:
    int choice(int n) const override {
        calls++;
        return n-1;
    }
};

std::unique_ptr<DummyRandomState> dummy_random_largest_ptr() {
    return std::unique_ptr<DummyRandomState>(dummy_random_largest());
}

TEST(IterativeStratificationPublic, MultilabelStratificationBalancedMulti) {
    MatrixInt labels = {{0, 1}, {1, 0}, {1, 1}, {0, 0}};
    VectorDouble r = {0.7, 0.3};
    auto rand = dummy_random_largest_ptr();
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    ASSERT_EQ(folds.size(), 4);
}

TEST(IterativeStratificationPublic, MoreFoldsThanSamples) {
    MatrixInt labels = {{0,0,0,0,1},{0,0,0,1,0},{0,0,1,0,0},{0,1,0,0,0},{1,0,0,0,0}};
    VectorDouble r = {1.0/5, 1.0/5, 1.0/5, 1.0/5, 1.0/5};
    auto rand = dummy_random_largest_ptr();
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    for (int f : folds) EXPECT_GE(f, 0), EXPECT_LT(f, 5);
}

TEST(IterativeStratificationPublic, AllZerosLabel) {
    MatrixInt labels(3, std::vector<int>(4, 0));
    VectorDouble r = {0.34, 0.33, 0.33};
    auto rand = dummy_random_largest_ptr();
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    for (int f : folds) EXPECT_TRUE(f==0||f==1||f==2);
}

TEST(IterativeStratificationPublic, FoldsShapeMatchesNSamples) {
    std::mt19937 rng(13);
    MatrixInt labels(7, std::vector<int>(4));
    for (int i=0; i<7; ++i) for (int j=0; j<4; ++j)
        labels[i][j] = rng() % 2;
    VectorDouble r = {0.3, 0.7};
    auto rand = dummy_random_largest_ptr();
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    ASSERT_EQ(folds.size(), 7);
}

TEST(IterativeStratificationPublic, InvalidFloatLabels) {
    std::vector<std::vector<float>> labels = {{0.2f, 1.0f}, {1.0f, 0.2f}};
    VectorDouble r = {0.6, 0.4};
    auto rand = dummy_random_largest_ptr();
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    }, std::out_of_range);
}

TEST(IterativeStratificationPublic, InvalidNonIntegerLabels) {
    std::vector<std::vector<float>> labels = {{0.5f},{0.5f},{0.5f},{0.0f}};
    VectorDouble r = {0.9, 0.1};
    auto rand = dummy_random_largest_ptr();
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    }, std::out_of_range);
}

TEST(IterativeStratificationPublic, BinaryStratificationSimpleFails) {
    MatrixInt labels = {{0},{1},{0},{1}};
    VectorDouble r = {0.5};
    auto rand = dummy_random_largest_ptr();
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    }, std::out_of_range);
}