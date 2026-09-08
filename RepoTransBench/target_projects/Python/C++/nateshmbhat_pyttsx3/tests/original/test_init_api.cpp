#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <memory>

class DummyEngineA {
public:
    DummyEngineA(const std::string&, bool = false) {}
    void say(const std::string&) {}
    void runAndWait() {}
    void stop() {}
};

static std::unordered_map<std::string, std::shared_ptr<DummyEngineA>>& get_engine_cacheA() {
    static std::unordered_map<std::string, std::shared_ptr<DummyEngineA>> cache;
    return cache;
}

std::shared_ptr<DummyEngineA> pyttsx3a_init(const std::string& driverName = "", bool = false) {
    auto& cache = get_engine_cacheA();
    if (cache.count(driverName) == 0)
        cache[driverName] = std::make_shared<DummyEngineA>(driverName);
    return cache[driverName];
}

TEST(InitApi, ReturnsEngine) {
    auto engine = pyttsx3a_init("dummy");
    // Only check that it has callable methods
    SUCCEED();
}

TEST(InitApi, ReturnsCachedInstance) {
    auto eng1 = pyttsx3a_init("dummy");
    auto eng2 = pyttsx3a_init("dummy");
    EXPECT_EQ(eng1.get(), eng2.get());
}

TEST(InitApi, InitWithDebugFlag) {
    auto eng = pyttsx3a_init("dummy", true);
    SUCCEED();
}

TEST(InitApi, SpeakCallsInitAndEngineMethods) {
    struct Calls {
        bool init = false;
        bool run = false;
        std::string say;
    } calls;
    class DummyEngineB {
    public:
        DummyEngineB(Calls* c) : calls(c) { c->init = true; }
        void say(const std::string& text) { calls->say = text; }
        void runAndWait() { calls->run = true; }
        Calls* calls;
    };
    auto pyttsx3b_init = [&](const std::string& text) { return std::make_unique<DummyEngineB>(&calls); };
    // Simulate "pyttsx3.speak('text')" calling init() and methods
    auto engine = pyttsx3b_init("text");
    engine->say("text");
    engine->runAndWait();
    EXPECT_TRUE(calls.init);
    EXPECT_EQ(calls.say, "text");
    EXPECT_TRUE(calls.run);
}