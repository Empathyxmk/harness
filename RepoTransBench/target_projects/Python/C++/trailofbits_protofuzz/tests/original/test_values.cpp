#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <cmath>
#include <set>
#include <algorithm>

// --- Stubs for protofuzz::values API ---
namespace values {
    struct integral_value_gen_t {
        std::vector<int> vals;
        size_t idx = 0;
        integral_value_gen_t() : vals({-10,-1,0,1,2,3,4,10}) {}
        int next() { if (idx>=vals.size()) throw std::out_of_range("done"); return vals[idx++]; }
    };
    struct float32_value_gen_t {
        std::vector<float> vals;
        size_t idx = 0;
        float32_value_gen_t() : vals({-3.7f, -0.42f, 0.f, 1.0f, 2.5f, 100.f, 9.f, -9.5f}) { }
        float next() { if (idx>=vals.size()) throw std::out_of_range("done"); return vals[idx++]; }
    };
    struct string_value_gen_t {
        std::vector<std::string> vals;
        size_t idx = 0;
        string_value_gen_t() : vals({"alpha", "beta", "", "test", "Z", "special$$"}) {}
        std::string next() { if (idx>=vals.size()) throw std::out_of_range("done"); return vals[idx++]; }
    };
    integral_value_gen_t integral_value_gen() { return {}; }
    float32_value_gen_t float32_value_gen() { return {}; }
    string_value_gen_t string_value_gen() { return {}; }
}
// ------------------------------------------

TEST(ValuesTest, IntegralValueGen) {
    auto g = values::integral_value_gen();
    std::vector<int> vals;
    for (int i=0; i<8; ++i) {
        vals.push_back(g.next());
    }
    for(auto v : vals) {
        EXPECT_TRUE(typeid(v)==typeid(int));
    }
}

TEST(ValuesTest, Float32ValueGen) {
    auto g = values::float32_value_gen();
    std::vector<float> vals;
    for (int i=0; i<8; ++i) {
        vals.push_back(g.next());
    }
    for(auto v : vals) {
        EXPECT_TRUE(typeid(v)==typeid(float));
    }
}

TEST(ValuesTest, StringValueGen) {
    auto g = values::string_value_gen();
    std::vector<std::string> vals;
    for (int i=0; i<6; ++i) {
        vals.push_back(g.next());
    }
    for(auto& v : vals) {
        EXPECT_TRUE(typeid(v)==typeid(std::string));
    }
}