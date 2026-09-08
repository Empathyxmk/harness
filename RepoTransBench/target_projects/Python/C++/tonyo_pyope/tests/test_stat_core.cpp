#include <gtest/gtest.h>
#include "stat.h"
#include "errors.h"

struct DummyRange {
    int start;
    int end;
    DummyRange(int s, int e) : start(s), end(e) {}
    int size() const { return end - start + 1; }
    bool contains(int value) const { return start <= value && value <= end; }
    DummyRange copy() const { return DummyRange(start, end); }
};

TEST(StatCore, SampleHgdEqualSize) {
    DummyRange in_r(10,20);
    DummyRange out_r(100,110);
    int nsample = 103;
    std::vector<int> coins = {0,1,0};
    auto in_size = [&](){return 11;};
    auto out_size = [&](){return 11;};
    auto out_contains = [&](int n){return 100 <= n && n <= 110;};
    int result = sample_hgd(
        in_r, out_r, 103, coins, in_size, out_size, out_contains
    );
    ASSERT_TRUE(typeid(result) == typeid(int));
}

TEST(StatCore, SampleHgdTypical) {
    DummyRange in_r(1,3);
    DummyRange out_r(10,15);
    int nsample = 13;
    std::vector<int> coins = {0,1,1};
    auto in_size = [&](){return 3;};
    auto out_size = [&](){return 6;};
    auto out_contains = [&](int n){return out_r.start <= n && n <= out_r.end;};

    // Monkeypatch: replace HGD::rhyper for this run ONLY
    auto rhyper_saved = HGD::rhyper;
    HGD::rhyper = [](int, int, int, const std::vector<int>&){ return 0; };
    EXPECT_EQ(sample_hgd(in_r, out_r, 13, coins, in_size, out_size, out_contains), 1);
    HGD::rhyper = [](int, int, int, const std::vector<int>&){ return 2; };
    EXPECT_EQ(sample_hgd(in_r, out_r, 13, coins, in_size, out_size, out_contains), 2);
    HGD::rhyper = rhyper_saved;
}

TEST(StatCore, SampleUniformWorks) {
    struct Range {
        int start, end;
        Range(int s, int e): start(s), end(e){}
        int size() const { return end - start + 1; }
        Range copy() const { return Range(start,end);}
    };
    Range r(10,11);
    std::vector<int> coins = {1};
    int val = sample_uniform(r, coins);
    EXPECT_TRUE(val == 10 || val == 11);
}

TEST(StatCore, SampleUniformNotEnoughCoins) {
    struct Range {
        int start, end;
        Range(int s, int e): start(s), end(e){}
        int size() const { return end - start + 1; }
        Range copy() const { return Range(start,end);}
    };
    Range r(1,2);
    std::vector<int> coins = {}; // not enough coins
    EXPECT_THROW(sample_uniform(r, coins), NotEnoughCoinsError);
}

TEST(StatCore, SampleUniformInvalidCoin) {
    struct Range {
        int start, end;
        Range(int s, int e): start(s), end(e){}
        int size() const { return end - start + 1; }
        Range copy() const { return Range(start,end);}
    };
    Range r(1,3);
    std::vector<int> coins = {7,0};
    EXPECT_THROW(sample_uniform(r, coins), InvalidCoinError);
}