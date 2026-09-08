#include <gtest/gtest.h>
#include <vector>
#include <algorithm>
#include <memory>
#include "iterative_stratification.hpp"

using MatrixInt = std::vector<std::vector<int>>;
using VectorDouble = std::vector<double>;

class DummyRandomStatePublic : public DummyRandomState {
public:
    int choice(int n) const override { calls++; return n-1; }
};

TEST(IterStratificationPublic, IterativeStratificationVaried_MainCase) {
    MatrixInt labels = {{0,1,0},{0,0,1},{1,1,0},{0,1,1},{1,0,1}};
    VectorDouble r = {0.7, 0.3};
    auto rs = std::make_unique<DummyRandomStatePublic>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    ASSERT_EQ(out.size(), labels.size());
    for (int f : out) EXPECT_TRUE(f==0||f==1);
}

TEST(IterStratificationPublic, IterativeStratificationVaried_XFail) {
    MatrixInt labels = {{0},{0},{1},{1}};
    VectorDouble r = {0.4, 0.6};
    auto rs = std::make_unique<DummyRandomStatePublic>();
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    }, std::out_of_range);
}

TEST(IterStratificationPublic, IterativeStratificationAllOnesLabel) {
    MatrixInt labels(4, std::vector<int>(3, 1));
    VectorDouble r = {0.2, 0.4, 0.4};
    auto rs = std::make_unique<DummyRandomStatePublic>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    ASSERT_EQ(out.size(), 4);
}

TEST(IterStratificationPublic, IterativeStratificationSingleFold) {
    MatrixInt labels = {{1,0,0,0,0},{0,1,0,0,0},{0,0,1,0,0},{0,0,0,1,0},{0,0,0,0,1}};
    VectorDouble r = {1.0};
    auto rs = std::make_unique<DummyRandomStatePublic>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    for (int f : out) EXPECT_EQ(f, 0);
}

TEST(IterStratificationPublic, IterativeStratificationRandomOutputTypes) {
    MatrixInt labels = {{0,1},{1,1}};
    VectorDouble r = {0.7, 0.3};
    auto rs = std::make_unique<DummyRandomStatePublic>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    for (int f : out) EXPECT_TRUE(typeid(f)==typeid(int));
}

TEST(IterStratificationPublic, IterativeStratificationAllZeroLabelsBranch) {
    MatrixInt labels(3, std::vector<int>(5, 0));
    VectorDouble r = {0.2, 0.2, 0.2, 0.2, 0.2};
    auto rs = std::make_unique<DummyRandomStatePublic>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    ASSERT_EQ(out.size(), 3);
    for (int f : out) EXPECT_GE(f, 0);
}