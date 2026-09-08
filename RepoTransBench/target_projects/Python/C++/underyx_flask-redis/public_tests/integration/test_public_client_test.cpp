#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <memory>

struct DummyRedisPub {
    static std::string called_with_url;
    static std::unordered_map<std::string, std::string> called_with_kwargs;
    static DummyRedisPub* from_url(const std::string& url, const std::unordered_map<std::string, std::string>& kwargs) {
        called_with_url = url;
        called_with_kwargs = kwargs;
        return new DummyRedisPub();
    }
};
std::string DummyRedisPub::called_with_url;
std::unordered_map<std::string, std::string> DummyRedisPub::called_with_kwargs;

struct AppSimPub {
    std::unordered_map<std::string, std::string> config;
    std::unordered_map<std::string, void*> extensions;
};

struct FlaskRedisPub {
    std::string config_prefix;
    DummyRedisPub* _redis_client = nullptr;
    using Provider = DummyRedisPub* (*)(const std::string&, const std::unordered_map<std::string, std::string>&);
    Provider provider_class = nullptr;

    explicit FlaskRedisPub(bool strict=false, const std::string& config_prefix_="") : config_prefix(config_prefix_) {}

    void init_app(AppSimPub* app, const std::unordered_map<std::string, std::string>& args = {}) {
        std::string key = config_prefix.empty() ? "REDIS_URL" : config_prefix + "_URL";
        std::string url = app->config[key];
        _redis_client = provider_class ? provider_class(url, args) : nullptr;
        std::string extkey = config_prefix.empty() ? "redis" : tolower(config_prefix);
        app->extensions[extkey] = this;
    }
    static std::string tolower(const std::string& str) {
        std::string res = str;
        for (auto& c : res) c = std::tolower(c);
        return res;
    }
    static FlaskRedisPub* from_custom_provider(Provider provider, AppSimPub* app, const std::unordered_map<std::string, std::string>& args) {
        auto* inst = new FlaskRedisPub();
        inst->provider_class = provider;
        inst->init_app(app, args);
        return inst;
    }
};

TEST(TestPublicIntegrationClient, test_init_app_custom_url_public) {
    FlaskRedisPub instance(false, "FOO");
    AppSimPub dummy_app;
    dummy_app.config["FOO_URL"] = "redis://localhost:6380/2";
    dummy_app.extensions = {};
    instance.provider_class = DummyRedisPub::from_url;
    instance.init_app(&dummy_app, {{"password", "letmein"}});
    EXPECT_EQ(DummyRedisPub::called_with_url, "redis://localhost:6380/2");
    EXPECT_EQ(DummyRedisPub::called_with_kwargs.at("password"), "letmein");
    EXPECT_TRUE(dummy_app.extensions.find("foo") != dummy_app.extensions.end());
    EXPECT_EQ(dummy_app.extensions["foo"], &instance);
}

TEST(TestPublicIntegrationClient, test_from_custom_provider_public) {
    struct CustomProvider {
        static std::string last_url;
        static std::unordered_map<std::string, std::string> last_kwargs;
        static DummyRedisPub* from_url(const std::string& url, const std::unordered_map<std::string, std::string>& kwargs) {
            last_url = url;
            last_kwargs = kwargs;
            return nullptr;
        }
    };
    std::string CustomProvider::last_url;
    std::unordered_map<std::string, std::string> CustomProvider::last_kwargs;
    AppSimPub dummy_app;
    dummy_app.config["REDIS_URL"] = "redis://localhost:6381/4";
    dummy_app.extensions = {};
    FlaskRedisPub* instance = FlaskRedisPub::from_custom_provider(CustomProvider::from_url, &dummy_app, {{"fooopt", "99"}});
    EXPECT_EQ(CustomProvider::last_url, "redis://localhost:6381/4");
    EXPECT_EQ(CustomProvider::last_kwargs.at("fooopt"), "99");
    EXPECT_TRUE(dummy_app.extensions.find("redis") != dummy_app.extensions.end());
    EXPECT_EQ(dummy_app.extensions["redis"], instance);
    delete instance;
}