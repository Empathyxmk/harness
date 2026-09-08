#include <gtest/gtest.h>
#include <string>
#include <map>
#include <any>
#include "memcacheify.h"

// This covers the classic unittest-style tests from tests.py

class MemcacheifyClassic : public ::testing::Test {
protected:
    std::map<std::string, std::string> saved_env;
    void SetUp() override {
        save_and_clear_env({
            "MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
            "MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
            "MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME"
        }, saved_env);
    }
    void TearDown() override { restore_env(saved_env); }
};

TEST_F(MemcacheifyClassic, test_uses_local_memory_backend_if_no_memcache_addon_is_available) {
    auto res = memcacheify();
    auto def = std::any_cast<SettingsMap>(res["default"]);
    EXPECT_EQ(std::any_cast<const char*>(def["BACKEND"]),
              BACKEND_LOC);
}

TEST_F(MemcacheifyClassic, tests_uses_local_memory_backend_if_one_of_the_memcache_env_vars_is_missing) {
    set_env("MEMCACHE_PASSWORD", "GCnQ9DhfEJqNDlo1");
    set_env("MEMCACHE_SERVERS", "mc3.ec2.northscale.net");
    auto res = memcacheify();
    auto def = std::any_cast<SettingsMap>(res["default"]);
    EXPECT_EQ(std::any_cast<const char*>(def["BACKEND"]),
              BACKEND_LOC);
    unset_env("MEMCACHE_PASSWORD");
    unset_env("MEMCACHE_SERVERS");
}

TEST_F(MemcacheifyClassic, test_sets_proper_backend_when_memcache_addon_is_available) {
    set_env("MEMCACHE_PASSWORD", "GCnQ9DhfEJqNDlo1");
    set_env("MEMCACHE_SERVERS", "mc3.ec2.northscale.net");
    set_env("MEMCACHE_USERNAME", "appxxxxx%40heroku.com");
    auto res = memcacheify();
    auto def = std::any_cast<SettingsMap>(res["default"]);
    EXPECT_EQ(std::any_cast<const char*>(def["BACKEND"]),
              BACKEND_PYLIBMC);
    unset_env("MEMCACHE_PASSWORD");
    unset_env("MEMCACHE_SERVERS");
    unset_env("MEMCACHE_USERNAME");
}

TEST_F(MemcacheifyClassic, test_uses_local_memory_backend_if_no_memcachier_addon_is_available) {
    set_env("MEMCACHIER_PASSWORD", "xxx");
    set_env("MEMCACHIER_SERVERS", "mc1.ec2.memcachier.com");
    auto res = memcacheify();
    auto def = std::any_cast<SettingsMap>(res["default"]);
    EXPECT_EQ(std::any_cast<const char*>(def["BACKEND"]), BACKEND_LOC);
    unset_env("MEMCACHIER_PASSWORD");
    unset_env("MEMCACHIER_SERVERS");
}

TEST_F(MemcacheifyClassic, test_sets_proper_backend_when_memcachier_addon_is_available) {
    set_env("MEMCACHIER_PASSWORD", "xxx");
    set_env("MEMCACHIER_SERVERS", "mc1.ec2.memcachier.com");
    set_env("MEMCACHIER_USERNAME", "xxx");

    auto caches = memcacheify();
    auto def = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(def["BACKEND"]), BACKEND_PYLIBMC);
    EXPECT_EQ(get_env("MEMCACHE_SERVERS"), get_env("MEMCACHIER_SERVERS"));
    EXPECT_EQ(get_env("MEMCACHE_USERNAME"), get_env("MEMCACHIER_USERNAME"));
    EXPECT_EQ(get_env("MEMCACHE_PASSWORD"), get_env("MEMCACHIER_PASSWORD"));

    unset_env("MEMCACHIER_PASSWORD");
    unset_env("MEMCACHIER_SERVERS");
    unset_env("MEMCACHIER_USERNAME");
    unset_env("MEMCACHE_PASSWORD");
    unset_env("MEMCACHE_SERVERS");
    unset_env("MEMCACHE_USERNAME");
}

TEST_F(MemcacheifyClassic, test_sets_proper_backend_when_memcachedcloud_addon_is_available) {
    set_env("MEMCACHEDCLOUD_PASSWORD", "xyz");
    set_env("MEMCACHEDCLOUD_SERVERS", "zzzz");
    set_env("MEMCACHEDCLOUD_USERNAME", "xyzzy");

    auto caches = memcacheify();
    auto def = std::any_cast<SettingsMap>(caches["default"]);
    EXPECT_EQ(std::any_cast<const char*>(def["BACKEND"]), BACKEND_PYLIBMC);
    EXPECT_EQ(get_env("MEMCACHE_SERVERS"), get_env("MEMCACHEDCLOUD_SERVERS"));
    EXPECT_EQ(get_env("MEMCACHE_USERNAME"), get_env("MEMCACHEDCLOUD_USERNAME"));
    EXPECT_EQ(get_env("MEMCACHE_PASSWORD"), get_env("MEMCACHEDCLOUD_PASSWORD"));

    unset_env("MEMCACHEDCLOUD_PASSWORD");
    unset_env("MEMCACHEDCLOUD_SERVERS");
    unset_env("MEMCACHEDCLOUD_USERNAME");
    unset_env("MEMCACHE_PASSWORD");
    unset_env("MEMCACHE_SERVERS");
    unset_env("MEMCACHE_USERNAME");
}