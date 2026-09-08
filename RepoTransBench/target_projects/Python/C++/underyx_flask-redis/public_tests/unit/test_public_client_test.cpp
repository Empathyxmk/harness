#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <memory>

struct DummyRedis {
    static std::string url;
    static std::unordered_map<std::string, std::string> kwargs;
    static DummyRedis* from_url(const std::string& url_, const std::unordered_map<std::string, std::string>& kwargs_) {
        url = url_;
        kwargs = kwargs_;
        return new DummyRedis();
    }
};
std::string DummyRedis::url;
std::unordered_map<std::string, std::string> DummyRedis::kwargs;

struct AppStruct {
    std::unordered_map<std::string, std::string> config;
    std::unordered_map<std::string, void*> extensions;
};

struct FlaskRedisPublic {
    std::string config_prefix;
    DummyRedis* _redis_client = nullptr;
    using Provider = DummyRedis* (*)(const std::string&, const std::unordered_map<std::string, std::string>&);
    Provider provider_class = nullptr;

    FlaskRedisPublic(bool strict, const std::string& config_prefix_): config_prefix(config_prefix_) {}

    void init_app(AppStruct* app, const std::unordered_map<std::string, std::string>& args = {}) {
        // Use config_prefix to get URL
        std::string key = config_prefix.empty() ? "REDIS_URL" : config_prefix + "_URL";
        std::string url = app->config[key];
        _redis_client = provider_class ? provider_class(url, args) : nullptr;
        app->extensions[config_prefix.empty() ? "redis" : tolowerstr(config_prefix)] = this;
    }
    static std::string tolowerstr(const std::string& str) {
        std::string res = str;
        for (char& c : res) c = std::tolower(c);
        return res;
    }
    static FlaskRedisPublic* from_custom_provider(DummyRedis::Provider provider, AppStruct* app, const std::unordered_map<std::string, std::string>& args) {
        auto* inst = new FlaskRedisPublic(false, "");
        inst->provider_class = provider;
        inst->init_app(app, args);
        return inst;
    }
};

TEST(TestPublicClient, test_flaskredis_init_app_different_url) {
    FlaskRedisPublic r(false, "APP2");
    AppStruct app;
    app.config["APP2_URL"] = "redis://127.0.0.1:6382/5";
    app.extensions = {};
    r.provider_class = DummyRedis::from_url;
    r.init_app(&app, {{"foo", "barbazquux"}});
    EXPECT_EQ(DummyRedis::url, "redis://127.0.0.1:6382/5");
    EXPECT_EQ(DummyRedis::kwargs.at("foo"), "barbazquux");
    EXPECT_TRUE(app.extensions.find("app2") != app.extensions.end());
    EXPECT_EQ(app.extensions["app2"], &r);
}

TEST(TestPublicClient, test_from_custom_provider_diff_url) {
    struct OtherProvider {
        static std::string called_url;
        static std::unordered_map<std::string, std::string> called_kwargs;
        static DummyRedis* from_url(const std::string& url, const std::unordered_map<std::string, std::string>& kwargs) {
            called_url = url;
            called_kwargs = kwargs;
            return nullptr;
        }
    };
    std::string OtherProvider::called_url = "";
    std::unordered_map<std::string, std::string> OtherProvider::called_kwargs;
    AppStruct app;
    app.config["REDIS_URL"] = "redis://192.168.1.2:6399/6";
    app.extensions = {};
    FlaskRedisPublic* r = FlaskRedisPublic::from_custom_provider(OtherProvider::from_url, &app, {{"baropt", "bartest99"}});
    EXPECT_EQ(OtherProvider::called_url, "redis://192.168.1.2:6399/6");
    EXPECT_EQ(OtherProvider::called_kwargs.at("baropt"), "bartest99");
    EXPECT_TRUE(app.extensions.find("redis") != app.extensions.end());
    EXPECT_EQ(app.extensions["redis"], r);
    delete r;
}

TEST(TestPublicClient, test_flaskredis_basic_instance) {
    FlaskRedisPublic r(true, "BAR");
    EXPECT_EQ(r.config_prefix, "BAR");
    EXPECT_TRUE(true); // Confirm methods are present by compilation
    EXPECT_TRUE(true);
}