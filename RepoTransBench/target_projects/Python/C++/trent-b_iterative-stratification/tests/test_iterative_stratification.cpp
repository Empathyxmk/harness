#include <gtest/gtest.h>
#include <vector>
#include <algorithm>
#include <memory>
#include "iterative_stratification.hpp"

using MatrixInt = std::vector<std::vector<int>>;
using VectorDouble = std::vector<double>;
using VectorInt = std::vector<int>;

class DummyRandomStateIter : public DummyRandomState {
public:
    int choice(int n) const override { calls++; return 0; }
};

TEST(IterStratOriginal, IterativeStratificationVaried_MainCase_1) {
    MatrixInt labels = {{1,0,1},{1,1,0},{0,1,1},{1,0,0},{0,0,0}};
    VectorDouble r = {0.6, 0.4};
    auto rs = std::make_unique<DummyRandomStateIter>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    ASSERT_EQ(out.size(), labels.size());
    for (int f : out) EXPECT_TRUE(f==0||f==1);
}

TEST(IterStratOriginal, IterativeStratificationVaried_XFail) {
    std::vector<std::vector<int>> labels = {{1},{1},{1},{0}};
    VectorDouble r = {0.5, 0.5};
    auto rs = std::make_unique<DummyRandomStateIter>();
    EXPECT_THROW({
        iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    }, std::out_of_range);
}

TEST(IterStratOriginal, IterativeStratificationAllOnesLabel) {
    MatrixInt labels(5, std::vector<int>(2, 1));
    VectorDouble r = {0.4, 0.6};
    auto rs = std::make_unique<DummyRandomStateIter>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    ASSERT_EQ(out.size(), 5);
}

TEST(IterStratOriginal, IterativeStratificationSingleFold) {
    MatrixInt labels = {{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}};
    VectorDouble r = {1.0};
    auto rs = std::make_unique<DummyRandomStateIter>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    for (int f : out) {
        EXPECT_EQ(f, 0);
    }
}

TEST(IterStratOriginal, IterativeStratificationRandomOutputTypes) {
    MatrixInt labels = {{1,0},{1,1}};
    VectorDouble r = {0.5, 0.5};
    auto rs = std::make_unique<DummyRandomStateIter>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    for (int f : out)
        EXPECT_TRUE(typeid(f)==typeid(int)); // Type check
}

TEST(IterStratOriginal, IterativeStratificationAllZeroLabelsBranch) {
    MatrixInt labels(4, std::vector<int>(2, 0));
    VectorDouble r = {0.25, 0.25, 0.25, 0.25};
    auto rs = std::make_unique<DummyRandomStateIter>();
    auto out = iterstrat::IterativeStratification::stratify(labels, r, rs.get());
    ASSERT_EQ(out.size(), 4);
    for (int f : out) EXPECT_GE(f, 0);
}