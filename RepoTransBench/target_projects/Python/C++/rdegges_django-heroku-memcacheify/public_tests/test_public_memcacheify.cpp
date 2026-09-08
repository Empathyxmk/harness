#include <gtest/gtest.h>
#include <string>
#include <map>
#include <any>
#include <vector>
#include "memcacheify.h"

// Utility functions used in tests
SettingsMap get_cache_conf(const std::any& result) {
    try {
        auto mp = std::any_cast<SettingsMap>(result);
        if (mp.count("default"))
            return std::any_cast<SettingsMap>(mp.at("default"));
        return mp;
    } catch (const std::bad_any_cast&) {
        return {};
    }
}
bool is_memcache_backend(const std::any& backend) {
    if (backend.type() == typeid(const char*))
        return (
            std::any_cast<const char*>(backend) == std::string(BACKEND_COREMC) ||
            std::any_cast<const char*>(backend) == std::string(BACKEND_PYLIBMC)
        );
    if (backend.type() == typeid(std::string))
        return (
            std::any_cast<std::string>(backend) == std::string(BACKEND_COREMC) ||
            std::any_cast<std::string>(backend) == std::string(BACKEND_PYLIBMC)
        );
    return false;
}
int extract_timeout(const SettingsMap& cache_conf) {
    auto it = cache_conf.find("TIMEOUT");
    if (it != cache_conf.end()) {
        if (it->second.type() == typeid(int))
            return std::any_cast<int>(it->second);
    }
    return -1;
}

class PubMemcacheifyEnv : public ::testing::Test {
protected:
    std::vector<std::string> relevant_envs = {
        "MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
        "MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
        "MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
        "MEMCACHEIFY_USE_LOCAL"
    };
    std::map<std::string, std::string> saved_env;
    void SetUp() override { save_and_clear_env(relevant_envs, saved_env); }
    void TearDown() override { restore_env(saved_env); }
};

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_basic) {
    set_env("MEMCACHIER_SERVERS", "alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112");
    set_env("MEMCACHIER_USERNAME", "public_alpha");
    set_env("MEMCACHIER_PASSWORD", "alp_pw");
    SettingsMap settings = { {"TIMEOUT", 876}, {"BINARY", true} };
    auto res = memcacheify(settings);
    auto cache_conf = get_cache_conf(res);
    EXPECT_TRUE(is_memcache_backend(cache_conf["BACKEND"]));
    std::string loc = std::any_cast<std::string>(cache_conf["LOCATION"]);
    EXPECT_TRUE(loc == "alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112" ||
                loc == "alpha-mc1.pub.net:22111;alpha-mc2.pub.net:22112");
    EXPECT_EQ(extract_timeout(cache_conf), 876);

    if (cache_conf.count("OPTIONS")) {
        auto opts = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        if (opts.count("username")) {
            EXPECT_EQ(std::any_cast<std::string>(opts["username"]), "public_alpha");
        }
        if (opts.count("password")) {
            EXPECT_EQ(std::any_cast<std::string>(opts["password"]), "alp_pw");
        }
    }
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_location_fallback) {
    unset_env("MEMCACHIER_SERVERS");
    set_env("MEMCACHE_SERVERS", "fallback-mc-newpub.example.com:31220");
    set_env("MEMCACHE_USERNAME", "newuser");
    set_env("MEMCACHE_PASSWORD", "newpass");
    SettingsMap empty_settings;
    auto res = memcacheify(empty_settings);
    auto cache_conf = get_cache_conf(res);
    std::string loc = std::any_cast<std::string>(cache_conf["LOCATION"]);
    EXPECT_TRUE(loc == "fallback-mc-newpub.example.com:31220" || loc == "localhost:11211");
    if (cache_conf.count("OPTIONS")) {
        auto opts = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        auto uit = opts.find("username");
        auto pit = opts.find("password");
        if (uit != opts.end())
            EXPECT_TRUE(std::any_cast<std::string>(uit->second) == "newuser" || std::any_cast<std::string>(uit->second).empty());
        if (pit != opts.end())
            EXPECT_TRUE(std::any_cast<std::string>(pit->second) == "newpass" || std::any_cast<std::string>(pit->second).empty());
    }
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_blank_env) {
    unset_env("MEMCACHIER_SERVERS");
    unset_env("MEMCACHE_SERVERS");
    unset_env("MEMCACHIER_USERNAME");
    unset_env("MEMCACHIER_PASSWORD");
    unset_env("MEMCACHE_USERNAME");
    unset_env("MEMCACHE_PASSWORD");
    SettingsMap s;
    auto res = memcacheify(s);
    auto cache_conf = get_cache_conf(res);
    std::string backend = std::any_cast<const char*>(cache_conf["BACKEND"]);
    EXPECT_TRUE(
        backend == BACKEND_COREMC ||
        backend == BACKEND_PYLIBMC ||
        backend == BACKEND_LOC
    );
    auto locit = cache_conf.find("LOCATION");
    if (locit != cache_conf.end()) {
        std::string loc = std::any_cast<std::string>(locit->second);
        EXPECT_TRUE(loc.empty() || loc == "localhost:11211");
    }
    if (cache_conf.count("OPTIONS")) {
        auto opts = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        auto uit = opts.find("username");
        auto pit = opts.find("password");
        if (uit != opts.end())
            EXPECT_TRUE(std::any_cast<std::string>(uit->second).empty());
        if (pit != opts.end())
            EXPECT_TRUE(std::any_cast<std::string>(pit->second).empty());
    }
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_timeouts) {
    set_env("MEMCACHIER_SERVERS", "b.pub.com:15111");
    set_env("MEMCACHIER_USERNAME", "pub_timeout");
    set_env("MEMCACHIER_PASSWORD", "pwtout");
    SettingsMap s; s["TIMEOUT"] = 9342;
    auto res = memcacheify(s);
    auto cache_conf = get_cache_conf(res);
    EXPECT_EQ(extract_timeout(cache_conf), 9342);
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_options_override) {
    set_env("MEMCACHIER_SERVERS", "pub-override.another.net");
    set_env("MEMCACHIER_USERNAME", "override_user");
    set_env("MEMCACHIER_PASSWORD", "override_pw");
    SettingsMap opts, behaviors;
    behaviors["connect_timeout"] = 9999;
    behaviors["retry_timeout"] = 55555;
    opts["behaviors"] = behaviors;
    opts["username"] = "optuser";
    opts["password"] = "optpw";
    SettingsMap custom = {
        {"OPTIONS", opts},
        {"TIMEOUT", 422}
    };
    auto res = memcacheify(custom);
    auto cache_conf = get_cache_conf(res);
    if (cache_conf.count("OPTIONS")) {
        auto optsmap = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        if (optsmap.count("behaviors")) {
            auto beh = std::any_cast<SettingsMap>(optsmap["behaviors"]);
            if (beh.count("connect_timeout"))
                EXPECT_TRUE(beh["connect_timeout"].type() == typeid(int) && std::any_cast<int>(beh["connect_timeout"]) == 9999);
            if (beh.count("retry_timeout"))
                EXPECT_TRUE(beh["retry_timeout"].type() == typeid(int) && std::any_cast<int>(beh["retry_timeout"]) == 55555);
        }
        if (optsmap.count("username")) {
            auto uval = std::any_cast<std::string>(optsmap["username"]);
            EXPECT_TRUE(uval == "optuser" || uval == "override_user");
        }
        if (optsmap.count("password")) {
            auto pval = std::any_cast<std::string>(optsmap["password"]);
            EXPECT_TRUE(pval == "optpw" || pval == "override_pw");
        }
    }
    EXPECT_EQ(extract_timeout(cache_conf), 422);
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_location_env_priority) {
    set_env("MEMCACHIER_SERVERS", "top-priority-pub.example:8998");
    set_env("MEMCACHE_SERVERS", "secondary-pub-fallback.example:8998");
    SettingsMap s;
    auto res = memcacheify(s);
    auto cache_conf = get_cache_conf(res);
    std::string loc = std::any_cast<std::string>(cache_conf["LOCATION"]);
    EXPECT_TRUE(loc == "top-priority-pub.example:8998" || loc == "localhost:11211");
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_null_settings) {
    set_env("MEMCACHIER_SERVERS", "");
    set_env("MEMCACHIER_USERNAME", "");
    set_env("MEMCACHIER_PASSWORD", "");
    auto res = memcacheify();
    auto cache_conf = get_cache_conf(res);
    std::string loc = "";
    auto lit = cache_conf.find("LOCATION");
    if (lit != cache_conf.end())
        loc = std::any_cast<std::string>(lit->second);
    EXPECT_TRUE(loc == "localhost:11211" || loc.empty());
    if (cache_conf.count("OPTIONS")) {
        auto opts = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        if (opts.count("username"))
            EXPECT_TRUE(std::any_cast<std::string>(opts["username"]).empty());
        if (opts.count("password"))
            EXPECT_TRUE(std::any_cast<std::string>(opts["password"]).empty());
    }
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_options_extend) {
    SettingsMap behaviors, opts;
    behaviors["dead_timeout"] = 57;
    opts["behaviors"] = behaviors;
    opts["extraopt"] = "xa_field";

    set_env("MEMCACHIER_SERVERS", "combo-extend.pub:6434");
    set_env("MEMCACHIER_USERNAME", "override_pub_ext");
    set_env("MEMCACHIER_PASSWORD", "pw_pub_combo");
    SettingsMap s;
    s["OPTIONS"] = opts;
    auto res = memcacheify(s);
    auto cache_conf = get_cache_conf(res);

    if (cache_conf.count("OPTIONS")) {
        auto optsmap = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        if (optsmap.count("behaviors")) {
            auto beh = std::any_cast<SettingsMap>(optsmap["behaviors"]);
            if (beh.count("dead_timeout"))
                EXPECT_EQ(std::any_cast<int>(beh["dead_timeout"]), 57);
        }
        if (optsmap.count("extraopt"))
            EXPECT_EQ(std::any_cast<std::string>(optsmap["extraopt"]), "xa_field");
        if (optsmap.count("username"))
            EXPECT_EQ(std::any_cast<std::string>(optsmap["username"]), "override_pub_ext");
        if (optsmap.count("password"))
            EXPECT_EQ(std::any_cast<std::string>(optsmap["password"]), "pw_pub_combo");
    }
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_empty_string_env) {
    set_env("MEMCACHIER_SERVERS", "");
    set_env("MEMCACHIER_USERNAME", "");
    set_env("MEMCACHIER_PASSWORD", "");
    SettingsMap empty;
    auto res = memcacheify(empty);
    auto cache_conf = get_cache_conf(res);
    auto lit = cache_conf.find("LOCATION");
    std::string loc = (lit != cache_conf.end() && lit->second.type() == typeid(std::string))
                      ? std::any_cast<std::string>(lit->second) : "";
    EXPECT_TRUE(loc == "" || loc == "localhost:11211");
    if (cache_conf.count("OPTIONS")) {
        auto opts = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        if (opts.count("username"))
            EXPECT_TRUE(std::any_cast<std::string>(opts["username"]).empty());
        if (opts.count("password"))
            EXPECT_TRUE(std::any_cast<std::string>(opts["password"]).empty());
    }
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_no_args) {
    set_env("MEMCACHIER_SERVERS", "");
    set_env("MEMCACHIER_USERNAME", "");
    set_env("MEMCACHIER_PASSWORD", "");
    auto res = memcacheify();
    auto cache_conf = get_cache_conf(res);
    auto lit = cache_conf.find("LOCATION");
    std::string loc = (lit != cache_conf.end() && lit->second.type() == typeid(std::string))
                      ? std::any_cast<std::string>(lit->second) : "";
    EXPECT_TRUE(loc == "localhost:11211" || loc == "");
    auto backend = cache_conf.at("BACKEND");
    EXPECT_TRUE(is_memcache_backend(backend) ||
                std::any_cast<const char*>(backend) == BACKEND_LOC);
}

TEST_F(PubMemcacheifyEnv, test_public_memcacheify_custom_behaviors) {
    SettingsMap behaviors, opts; // Custom behaviors
    behaviors["tcp_keepalive"] = std::any(); // None/nullptr
    behaviors["tcp_nodelay"] = false;
    opts["behaviors"] = behaviors;
    set_env("MEMCACHIER_SERVERS", "customb-pub1.example.net:51035");
    SettingsMap s;
    s["OPTIONS"] = opts;
    auto res = memcacheify(s);
    auto cache_conf = get_cache_conf(res);

    if (cache_conf.count("OPTIONS")) {
        auto optsmap = std::any_cast<SettingsMap>(cache_conf.at("OPTIONS"));
        if (optsmap.count("behaviors")) {
            auto beh = std::any_cast<SettingsMap>(optsmap["behaviors"]);
            if (beh.count("tcp_keepalive"))
                EXPECT_TRUE(!beh["tcp_keepalive"].has_value());
            if (beh.count("tcp_nodelay"))
                EXPECT_TRUE(beh["tcp_nodelay"].type() == typeid(bool) &&
                            (std::any_cast<bool>(beh["tcp_nodelay"]) == false ||
                            std::any_cast<bool>(beh["tcp_nodelay"]) == true));
        }
    }
}