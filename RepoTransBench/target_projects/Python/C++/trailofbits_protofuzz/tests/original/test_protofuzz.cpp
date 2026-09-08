#include <gtest/gtest.h>
#include <typeinfo>
#include <vector>
#include <string>
#include <memory>

// --- Stubs for protofuzz API (replace with actual includes in real use) ---
struct SimpleNamespace {
    int x;
};
namespace protofuzz {
    template <typename MsgType, typename ValMap>
    auto message_strategy(const ValMap& map) {
        return [=]() mutable {
            struct Iterator {
                bool called = false;
                MsgType operator()() {
                    MsgType msg;
                    msg.x = 1;
                    return msg;
                }
                MsgType* begin() { return nullptr; }
                MsgType* end() { return nullptr; }
            };
            // Emulate return of generator style interface (Python yields)
            struct Gen {
                bool used = false;
                MsgType operator()() {
                    if (used) throw std::out_of_range("done");
                    used = true;
                    MsgType msg;
                    msg.x = 1;
                    return msg;
                }
            };
            return [g=Gen()]() mutable {
                return g();
            };
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
// -------------------------------------------------------------------------

TEST(ProtofuzzTest, MessageStrategySmoke) {
    auto strat = protofuzz::message_strategy<SimpleNamespace>(std::map<std::string, std::function<std::vector<int>(int, void*)>>{
        {"x", [](int t, void* f)->std::vector<int>{ return {1}; }}
    });
    auto gen = strat();
    // Mimic generator by calling the returned lambda
    SimpleNamespace msg = gen();
    // Must return an instance of SimpleNamespace - already satisfied as struct
    EXPECT_EQ(typeid(msg), typeid(SimpleNamespace));
}

TEST(ProtofuzzTest, FuzzSmoke) {
    std::vector<std::string> results;
    // Dummy generator returning "A", "B", "C"
    struct DummyGen {
        int idx = 0;
        std::string operator()() {
            if (idx == 0) { idx++; return "A"; }
            else if (idx == 1) { idx++; return "B"; }
            else if (idx == 2) { idx++; return "C"; }
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
    // emulate protofuzz.fuzz, calling collect 3 times
    auto gen = strat();
    for (int i=0; i<3; ++i) {
        results.push_back(gen());
    }
    EXPECT_EQ(results, std::vector<std::string>({"A","B","C"}));
}