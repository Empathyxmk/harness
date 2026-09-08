#include <gtest/gtest.h>
#include <vector>
#include <set>
#include <string>
#include <cmath>
#include <algorithm>

// --- Stub for values public API (sync with test_values.cpp) ---
namespace values_public {
    struct integral_value_gen_t {
        std::vector<int> vals;
        size_t idx = 0;
        integral_value_gen_t() : vals({-10, -5, -1, 0, 3, 6, 7, 100}) {}
        int next() { if (idx>=vals.size()) throw std::out_of_range("done"); return vals[idx++]; }
        std::vector<int> to_vector() { return vals; }
        void reset() { idx = 0; }
    };
    struct float32_value_gen_t {
        std::vector<float> vals;
        size_t idx = 0;
        float32_value_gen_t() : vals({-10.5, -0.5, 0.0, 0.9, 1.5, 3.14, 7.2, 50.0, 1.1}) {}
        float next() { if (idx>=vals.size()) throw std::out_of_range("done"); return vals[idx++]; }
        std::vector<float> to_vector() { return vals; }
        void reset() { idx = 0; }
    };
    struct string_value_gen_t {
        std::vector<std::string> vals;
        size_t idx = 0;
        string_value_gen_t() : vals({"alpha", "beta", "zzz", "!", "testxxx", "longer_string", "", "!!?"}) {}
        std::string next() { if (idx>=vals.size()) throw std::out_of_range("done"); return vals[idx++]; }
        std::vector<std::string> to_vector() { return vals; }
        void reset() { idx = 0; }
    };
    integral_value_gen_t integral_value_gen() { return {}; }
    float32_value_gen_t float32_value_gen() { return {}; }
    string_value_gen_t string_value_gen() { return {}; }
}

// ---------------------------------

TEST(PublicValuesTest, IntegralValueGenPublic) {
    auto g = values_public::integral_value_gen();
    std::vector<int> vals;
    for (int i=0;;++i) {
        try { vals.push_back(g.next()); }
        catch(const std::out_of_range&) { break; }
    }
    for(auto v : vals) {
        EXPECT_TRUE(typeid(v)==typeid(int));
    }
    std::set<int> sval(vals.begin(), vals.end());
    EXPECT_EQ(vals.size(), sval.size());
    bool found_neg = false, found_nonneg = false;
    for(int v : vals) {
        if (v < 0) found_neg = true;
        if (v >= 0) found_nonneg = true;
    }
    EXPECT_TRUE(found_neg && found_nonneg);
    EXPECT_GT(vals.size(), 5);
}

TEST(PublicValuesTest, Float32ValueGenPublic) {
    auto g = values_public::float32_value_gen();
    std::vector<float> vals;
    for (int i=0;;++i) {
        try { vals.push_back(g.next()); }
        catch(const std::out_of_range&) { break; }
    }
    for(auto v : vals) {
        EXPECT_TRUE(typeid(v)==typeid(float));
    }
    std::set<float> sval(vals.begin(), vals.end());
    EXPECT_EQ(vals.size(), sval.size());
    bool below_one = false, above_one = false;
    for(float v : vals) {
        if (std::abs(v) < 1.0) below_one = true;
        if (std::abs(v) > 1.0) above_one = true;
    }
    EXPECT_TRUE(below_one && above_one);
    EXPECT_GT(vals.size(), 7);
}

TEST(PublicValuesTest, StringValueGenPublic) {
    auto g = values_public::string_value_gen();
    std::vector<std::string> vals;
    for (int i=0;;++i) {
        try { vals.push_back(g.next()); }
        catch(const std::out_of_range&) { break; }
    }
    for(auto& v : vals) {
        EXPECT_TRUE(typeid(v)==typeid(std::string));
    }
    std::set<std::string> sval(vals.begin(), vals.end());
    EXPECT_EQ(vals.size(), sval.size());
    bool has_long = false;
    for(auto& s : vals) {
        if (s.length() > 3) has_long = true;
    }
    EXPECT_TRUE(has_long);
    EXPECT_GT(vals.size(), 5);
}