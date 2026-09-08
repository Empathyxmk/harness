#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <memory>
#include <algorithm>

// Public test: Monkey-patching "init" and dummy engine logic

class AnotherDummyEngine {
public:
    std::string driverName;
    AnotherDummyEngine(std::string drv = "") : driverName(drv) {}
    std::string say(const std::string& text) { std::string r = text; std::reverse(r.begin(), r.end()); return r; }
    std::string runAndWait() { return "executed"; }
    std::string stop() { return "halted"; }
};

static std::unordered_map<std::string, std::shared_ptr<AnotherDummyEngine>>& get_public_engine_cache() {
    static std::unordered_map<std::string, std::shared_ptr<AnotherDummyEngine>> cache;
    return cache;
}

std::shared_ptr<AnotherDummyEngine> pyttsx3_public_init(const std::string& driverName = "") {
    auto& cache = get_public_engine_cache();
    if (cache.count(driverName) == 0)
        cache[driverName] = std::make_shared<AnotherDummyEngine>(driverName);
    return cache[driverName];
}

TEST(PublicPyttsx3, InitAndEngine) {
    auto engine = pyttsx3_public_init("diffdummy");
    EXPECT_EQ(engine->driverName, "diffdummy");
}

TEST(PublicPyttsx3, EngineCache) {
    auto e1 = pyttsx3_public_init("cachetestA");
    auto e2 = pyttsx3_public_init("cachetestA");
    EXPECT_EQ(e1.get(), e2.get());
}

TEST(PublicPyttsx3, EngineUnique) {
    auto e1 = pyttsx3_public_init("uniqueA");
    auto e2 = pyttsx3_public_init("uniqueB");
    EXPECT_NE(e1.get(), e2.get());
}

TEST(PublicPyttsx3, EngineMethods) {
    auto e1 = pyttsx3_public_init("diffdummy");
    EXPECT_EQ(e1->say("bar"), "rab");
    EXPECT_EQ(e1->runAndWait(), "executed");
    EXPECT_EQ(e1->stop(), "halted");
}