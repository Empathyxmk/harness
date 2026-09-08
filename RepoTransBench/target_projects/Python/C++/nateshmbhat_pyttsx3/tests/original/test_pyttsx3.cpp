#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <memory>

// Dummy stub for pyttsx3::Engine
class DummyEngine {
public:
    std::string driverName;
    DummyEngine(std::string drv = "") : driverName(drv) {}
    std::string say(const std::string& text) { return text; }
    std::string runAndWait() { return "ran"; }
    std::string stop() { return "stopped"; }
    int dummy_method() { return 42; }
};

static std::unordered_map<std::string, std::shared_ptr<DummyEngine>>& get_engine_cache() {
    static std::unordered_map<std::string, std::shared_ptr<DummyEngine>> cache;
    return cache;
}

std::shared_ptr<DummyEngine> pyttsx3_init(const std::string& driverName = "") {
    auto& cache = get_engine_cache();
    if (cache.count(driverName) == 0)
        cache[driverName] = std::make_shared<DummyEngine>(driverName);
    return cache[driverName];
}

TEST(Pyttsx3, InitAndEngine) {
    auto engine = pyttsx3_init("dummy");
    EXPECT_EQ(engine->driverName, "dummy");
}

TEST(Pyttsx3, EngineCache) {
    auto e1 = pyttsx3_init("dummy");
    auto e2 = pyttsx3_init("dummy");
    EXPECT_EQ(e1.get(), e2.get());
}

TEST(Pyttsx3, EngineUnique) {
    auto e1 = pyttsx3_init("dummy1");
    auto e2 = pyttsx3_init("dummy2");
    EXPECT_NE(e1.get(), e2.get());
}

TEST(Pyttsx3, EngineMethods) {
    auto e1 = pyttsx3_init("dummy");
    EXPECT_EQ(e1->say("foo"), "foo");
    EXPECT_EQ(e1->runAndWait(), "ran");
    EXPECT_EQ(e1->stop(), "stopped");
}