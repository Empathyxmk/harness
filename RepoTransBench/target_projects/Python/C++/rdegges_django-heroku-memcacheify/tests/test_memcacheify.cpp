#include <gtest/gtest.h>
#include <string>
#include <map>
#include <any>
#include <vector>
#include "memcacheify.h"

static const std::vector<std::string> relevant_envs = {
    "MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
    "MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
    "MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
    "MEMCACHEIFY_USE_LOCAL"
};

class CleanEnviron : public ::testing::Test {
protected:
    std::map<std::string, std::string> saved_env;
    void SetUp() override { save_and_clear_env(relevant_envs, saved_env); }
    void TearDown() override { restore_env(saved_env); }
};

TEST_F(CleanEnviron, test_local_cache_default) {
    auto caches = memcacheify();
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_LOC);
}

TEST_F(CleanEnviron, test_memcache_env_vars_missing) {
    set_env("MEMCACHE_PASSWORD", "pass");
    set_env("MEMCACHE_SERVERS", "host");
    // username missing
    auto caches = memcacheify();
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_LOC);
}

TEST_F(CleanEnviron, test_memcache_env_vars_set) {
    set_env("MEMCACHE_PASSWORD", "pass");
    set_env("MEMCACHE_SERVERS", "host");
    set_env("MEMCACHE_USERNAME", "user");
    SettingsMap settings; settings["TIMEOUT"] = 111;
    auto caches = memcacheify(settings);
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_PYLIBMC);
    EXPECT_EQ(std::any_cast<std::string>(default_cache["LOCATION"]), "host");
    EXPECT_EQ(std::any_cast<int>(default_cache["TIMEOUT"]), 111);
}

TEST_F(CleanEnviron, test_memcachier_env_vars_set) {
    set_env("MEMCACHIER_PASSWORD", "pw");
    set_env("MEMCACHIER_SERVERS", "host1,host2");
    set_env("MEMCACHIER_USERNAME", "user");
    SettingsMap settings; settings["TIMEOUT"] = 123;
    auto caches = memcacheify(settings);
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_TRUE(default_cache["LOCATION"] == std::string("host1;host2") || default_cache["LOCATION"] == std::string("host1,host2"));
    EXPECT_EQ(std::any_cast<int>(default_cache["TIMEOUT"]), 123);
    EXPECT_EQ(get_env("MEMCACHE_SERVERS"), "host1,host2");
    EXPECT_EQ(get_env("MEMCACHE_USERNAME"), "user");
    EXPECT_EQ(get_env("MEMCACHE_PASSWORD"), "pw");
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_PYLIBMC);
}

TEST_F(CleanEnviron, test_memcachedcloud_env_vars_set) {
    set_env("MEMCACHEDCLOUD_PASSWORD", "pwcloud");
    set_env("MEMCACHEDCLOUD_SERVERS", "c1,c2");
    set_env("MEMCACHEDCLOUD_USERNAME", "clouduser");
    SettingsMap settings; settings["TIMEOUT"] = 321;
    auto caches = memcacheify(settings);
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_TRUE(default_cache["LOCATION"] == std::string("c1;c2") || default_cache["LOCATION"] == std::string("c1,c2"));
    EXPECT_EQ(std::any_cast<int>(default_cache["TIMEOUT"]), 321);
    EXPECT_EQ(get_env("MEMCACHE_SERVERS"), "c1,c2");
    EXPECT_EQ(get_env("MEMCACHE_USERNAME"), "clouduser");
    EXPECT_EQ(get_env("MEMCACHE_PASSWORD"), "pwcloud");
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_PYLIBMC);
}

TEST_F(CleanEnviron, test_memcacheify_use_local) {
    set_env("MEMCACHEIFY_USE_LOCAL", "1");
    auto caches = memcacheify();
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_PYLIBMC);
}

struct ParamedMemcachierIncomplete
    : public CleanEnviron,
      public ::testing::WithParamInterface<std::vector<std::string>> {};

TEST_P(ParamedMemcachierIncomplete, test_memcachier_incomplete) {
    set_env("MEMCACHIER_PASSWORD", "pw");
    set_env("MEMCACHIER_SERVERS", "h1");
    set_env("MEMCACHIER_USERNAME", "u1");
    for (const auto& m : GetParam()) unset_env(m);
    auto caches = memcacheify();
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_LOC);
}
INSTANTIATE_TEST_SUITE_P(MemcachierParams, ParamedMemcachierIncomplete, ::testing::Values(
    std::vector<std::string>{"MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS"},
    std::vector<std::string>{"MEMCACHIER_PASSWORD"}
));

struct ParamedMemcachedCloudIncomplete
    : public CleanEnviron,
      public ::testing::WithParamInterface<std::vector<std::string>> {};

TEST_P(ParamedMemcachedCloudIncomplete, test_memcachedcloud_incomplete) {
    set_env("MEMCACHEDCLOUD_PASSWORD", "pw");
    set_env("MEMCACHEDCLOUD_SERVERS", "h1");
    set_env("MEMCACHEDCLOUD_USERNAME", "u1");
    for (const auto& m : GetParam()) unset_env(m);
    auto caches = memcacheify();
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(default_cache["BACKEND"]), BACKEND_LOC);
}
INSTANTIATE_TEST_SUITE_P(CloudParams, ParamedMemcachedCloudIncomplete, ::testing::Values(
    std::vector<std::string>{"MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS"},
    std::vector<std::string>{"MEMCACHEDCLOUD_PASSWORD"}
));

TEST_F(CleanEnviron, test_memcacheify_timeout_default) {
    set_env("MEMCACHE_PASSWORD", "p");
    set_env("MEMCACHE_SERVERS", "h");
    set_env("MEMCACHE_USERNAME", "u");
    auto caches = memcacheify();
    auto default_cache = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<int>(default_cache["TIMEOUT"]), 500);
}