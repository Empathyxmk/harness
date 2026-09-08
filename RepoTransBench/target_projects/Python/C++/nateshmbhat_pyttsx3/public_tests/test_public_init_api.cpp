#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <memory>

class YetAnotherDummyEngine {
public:
    std::string name;
    YetAnotherDummyEngine(std::string driverName = "", bool debug = false) : name(driverName) {}
    std::string start() { return "hello"; }
    std::string finish() { return "goodbye"; }
};

static std::unordered_map<std::string, std::shared_ptr<YetAnotherDummyEngine>>& get_public_engine_cache() {
    static std::unordered_map<std::string, std::shared_ptr<YetAnotherDummyEngine>> cache;
    return cache;
}

std::shared_ptr<YetAnotherDummyEngine> pyttsx3_public_init(const std::string& driverName = "") {
    auto& cache = get_public_engine_cache();
    if (cache.count(driverName) == 0)
        cache[driverName] = std::make_shared<YetAnotherDummyEngine>(driverName);
    return cache[driverName];
}

TEST(PublicInitApi, EngineCreation) {
    auto engine = pyttsx3_public_init("publicengine");
    EXPECT_EQ(engine->name, "publicengine");
}

TEST(PublicInitApi, EngineSingleton) {
    auto e1 = pyttsx3_public_init("publicdummyA");
    auto e2 = pyttsx3_public_init("publicdummyA");
    EXPECT_EQ(e1.get(), e2.get());
}

TEST(PublicInitApi, EngineDifferent) {
    auto e1 = pyttsx3_public_init("public1");
    auto e2 = pyttsx3_public_init("public2");
    EXPECT_NE(e1.get(), e2.get());
}