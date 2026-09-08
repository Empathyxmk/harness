#include <gtest/gtest.h>
#include <vector>
#include <algorithm>
#include <memory>
#include <random>
#include "iterative_stratification.hpp"

// Simulate numpy array creation helpers.
using MatrixInt = std::vector<std::vector<int>>;
using VectorDouble = std::vector<double>;
using VectorInt = std::vector<int>;

TEST(IterativeStratificationOriginal, MultilabelStratificationBalancedMulti) {
    MatrixInt labels = {{1, 0}, {1, 1}, {0, 1}, {0, 0}};
    VectorDouble r = {0.5, 0.5};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    ASSERT_EQ(folds.size(), 4);
}

TEST(IterativeStratificationOriginal, MoreFoldsThanSamples) {
    MatrixInt labels = {{1,0,0,0,0,0},{0,1,0,0,0,0},{0,0,1,0,0,0},{0,0,0,1,0,0},{0,0,0,0,1,0},{0,0,0,0,0,1}};
    VectorDouble r = {1.0/6, 1.0/6, 1.0/6, 1.0/6, 1.0/6, 1.0/6};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    for (int f : folds) {
        EXPECT_GE(f, 0);
        EXPECT_LT(f, 6);
    }
}

TEST(IterativeStratificationOriginal, AllZerosLabel) {
    MatrixInt labels(4, std::vector<int>(2, 0));
    VectorDouble r = {0.5, 0.5};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    for (int f : folds) {
        EXPECT_TRUE(f == 0 || f == 1);
    }
}

TEST(IterativeStratificationOriginal, FoldsShapeMatchesNSamples) {
    std::mt19937 rng(42);
    MatrixInt labels(10, std::vector<int>(3));
    for (int i=0; i<10; ++i)
        for (int j=0; j<3; ++j)
            labels[i][j] = rng() % 2;
    VectorDouble r = {0.6, 0.4};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    auto folds = iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    ASSERT_EQ(folds.size(), 10);
}

TEST(IterativeStratificationOriginal, InvalidFloatLabels) {
    std::vector<std::vector<float>> labels = {{1.0f, 0.0f}, {0.0f, 1.0f}};
    VectorDouble r = {0.5, 0.5};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    }, std::out_of_range);
}

TEST(IterativeStratificationOriginal, InvalidNonIntegerLabels) {
    std::vector<std::vector<float>> labels = {{0.8f}, {0.8f}, {0.2f}, {0.0f}};
    VectorDouble r = {0.5, 0.5};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    }, std::out_of_range);
}

TEST(IterativeStratificationOriginal, BinaryStratificationSimple) {
    MatrixInt labels = {{1},{0},{1},{0}};
    VectorDouble r = {0.5};
    std::unique_ptr<DummyRandomState> rand(dummy_random_smallest());
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rand.get());
    }, std::out_of_range);
}