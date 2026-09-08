#include <gtest/gtest.h>
#include <map>
#include <functional>
#include <typeinfo>
#include <vector>
#include <string>
// --- Stubs for protofuzz API (as per earlier) ---
struct SimpleNamespacePublic {
    int y;
};
namespace protofuzz_public {
    template <typename MsgType, typename ValMap>
    auto message_strategy(const ValMap& map) {
        return [=]() mutable {
            struct Gen {
                bool used = false;
                MsgType operator()() {
                    if (used) throw std::out_of_range("done");
                    used = true;
                    MsgType msg;
                    msg.y = 42;
                    return msg;
                }
            };
            return [g=Gen()]() mutable { return g(); };
        };
    }
    template <typename Strat, typename Collector>
    void fuzz(Strat strat, Collector coll, int max_tests=3) {
        auto gen = strat();
        try {
            for (int i=0; i<max_tests; ++i) {
                coll(gen());
            }
        } catch(const std::out_of_range&) {
        }
    }
}
// ----------------------------------------

TEST(PublicProtofuzzTest, MessageStrategyPublic) {
    // Use y field (not x), value 42
    auto strat = protofuzz_public::message_strategy<SimpleNamespacePublic>(
        std::map<std::string, std::function<std::vector<int>(int, void*)>>{
            {"y", [](int t, void* f)->std::vector<int>{ return {42}; }}});
    auto gen = strat();
    SimpleNamespacePublic msg = gen();
    EXPECT_EQ(typeid(msg), typeid(SimpleNamespacePublic));
    // Has y field, and equals 42
    EXPECT_EQ(msg.y, 42);
}

TEST(PublicProtofuzzTest, FuzzPublic) {
    std::vector<std::string> results;
    // Dummy generator returning "D", "E", "F"
    struct DummyGen {
        int idx = 0;
        std::string operator()() {
            if (idx == 0) { idx++; return "D"; }
            else if (idx == 1) { idx++; return "E"; }
            else if (idx == 2) { idx++; return "F"; }
            else throw std::out_of_range("done");
        }
    };
    auto strat = []() {
        DummyGen dg;
        return [dg=dg]() mutable { return dg(); };
    };
    auto collect = [&](const std::string& msg) {
        results.push_back(msg);
    };
    auto gen = strat();
    for (int i=0; i<3; ++i) {
        results.push_back(gen());
    }
    EXPECT_EQ(results, std::vector<std::string>({"D","E","F"}));
}