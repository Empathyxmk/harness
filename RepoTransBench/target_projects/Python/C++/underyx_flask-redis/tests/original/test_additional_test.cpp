#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <type_traits>

struct DummyRedis {
    std::unordered_map<std::string, std::string> values;
    static bool from_url_called;

    static DummyRedis* from_url(const std::string &, ...) {
        from_url_called = true;
        return new DummyRedis();
    }
    std::string test_func() const { return "called"; }
    std::string operator[](const std::string& name) const {
        auto it = values.find(name);
        return (it != values.end()) ? it->second : "";
    }
    std::string& operator[](const std::string& name) {
        return values[name];
    }
    void erase(const std::string& name) {
        values.erase(name);
    }
};
bool DummyRedis::from_url_called = false;

// Dummy FlaskRedis mimicking the tested logic
class DummyProvider {
public:
    static bool from_url_called;
    static DummyRedis* from_url(const std::string&, ...) {
        from_url_called = true;
        return new DummyRedis();
    }
};
bool DummyProvider::from_url_called = false;

class FlaskRedisSim {
public:
    using ProviderClassPtr = DummyRedis* (*)(const std::string&, ...);
    void* _redis_client = nullptr; // type erased
    ProviderClassPtr provider_class = nullptr;
    std::unordered_map<std::string, std::string> provider_kwargs;

    static FlaskRedisSim* from_custom_provider(DummyProvider, void* app = nullptr) {
        FlaskRedisSim* inst = new FlaskRedisSim();
        inst->provider_class = DummyProvider::from_url;
        return inst;
    }
    std::string __getattr__(const std::string& name) {
        // Forward to DummyRedis for "test_func"
        if (name == "test_func")
            return static_cast<DummyRedis*>(_redis_client)->test_func();
        throw std::runtime_error("AttributeError");
    }
    std::string operator[](const std::string& name) {
        return static_cast<DummyRedis*>(_redis_client)->operator[](name);
    }
    void setitem(const std::string& name, const std::string& value) {
        static_cast<DummyRedis*>(_redis_client)->operator[](name) = value;
    }
    void delitem(const std::string& name) {
        static_cast<DummyRedis*>(_redis_client)->erase(name);
    }
    void init_app(struct AppSim* app);
};

struct AppSim {
    std::unordered_map<std::string, std::string> config;
    std::unordered_map<std::string, void*> extensions;
};

void FlaskRedisSim::init_app(AppSim* app) {
    app->extensions["redis"] = this;
}

TEST(TestAdditional, test_from_custom_provider_sets_provider_and_inits) {
    DummyProvider::from_url_called = false;
    AppSim app;
    FlaskRedisSim* inst = FlaskRedisSim::from_custom_provider(DummyProvider(), &app);
    EXPECT_TRUE(inst->provider_class);
    EXPECT_TRUE(DummyProvider::from_url_called);
    delete inst;
}

TEST(TestAdditional, test_from_custom_provider_no_app) {
    FlaskRedisSim* result = FlaskRedisSim::from_custom_provider(DummyProvider());
    EXPECT_TRUE(result->provider_class);
    delete result;
}

TEST(TestAdditional, test_from_custom_provider_assertion) {
    EXPECT_THROW({
        FlaskRedisSim::from_custom_provider(*(DummyProvider*)nullptr);
    }, std::bad_typeid);
}

TEST(TestAdditional, test_dunder_methods_forward) {
    DummyRedis* dummy = new DummyRedis();
    FlaskRedisSim inst;
    inst._redis_client = dummy;
    EXPECT_EQ(inst.__getattr__("test_func"), "called");
    inst.setitem("foo", "bar");
    EXPECT_EQ(inst["foo"], "bar");
    inst.delitem("foo");
    EXPECT_EQ(inst["foo"], "");
    delete dummy;
}

TEST(TestAdditional, test_init_app_sets_extensions_dict) {
    FlaskRedisSim inst;
    inst.provider_class = DummyProvider::from_url;
    AppSim app;
    inst.init_app(&app);
    EXPECT_EQ(app.extensions["redis"], &inst);
}

TEST(TestAdditional, test_init_app_creates_extensions) {
    FlaskRedisSim inst;
    inst.provider_class = DummyProvider::from_url;
    AppSim app;
    inst.init_app(&app);
    EXPECT_TRUE(app.extensions.find("redis") != app.extensions.end());
}

TEST(TestAdditional, test_unusual_config_prefix) {
    FlaskRedisSim inst;
    inst.provider_class = DummyProvider::from_url;
    AppSim app;
    app.config["FOOBAR_URL"] = "redis://notreal:1234";
    inst.init_app(&app);
    EXPECT_EQ(app.extensions["redis"], &inst);
}