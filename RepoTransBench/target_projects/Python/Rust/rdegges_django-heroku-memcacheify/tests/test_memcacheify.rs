use std::collections::HashMap;
use std::sync::Mutex;

use serial_test::serial;

use django_heroku_memcacheify::{memcacheify, memcacheify_with_timeout, CacheConf};

fn clean_env() {
    let keys = [
        "MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
        "MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
        "MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
        "MEMCACHEIFY_USE_LOCAL"
    ];
    for k in keys.iter() {
        std::env::remove_var(k);
    }
}

#[test]
#[serial]
fn test_local_cache_default() {
    clean_env();
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django.core.cache.backends.locmem.LocMemCache");
}

#[test]
#[serial]
fn test_memcache_env_vars_missing() {
    clean_env();
    std::env::set_var("MEMCACHE_PASSWORD", "pass");
    std::env::set_var("MEMCACHE_SERVERS", "host");
    // username missing
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django.core.cache.backends.locmem.LocMemCache");
}

#[test]
#[serial]
fn test_memcache_env_vars_set() {
    clean_env();
    std::env::set_var("MEMCACHE_PASSWORD", "pass");
    std::env::set_var("MEMCACHE_SERVERS", "host");
    std::env::set_var("MEMCACHE_USERNAME", "user");
    let caches = memcacheify_with_timeout(111);
    assert_eq!(caches["default"].BACKEND, "django_pylibmc.memcached.PyLibMCCache");
    assert_eq!(caches["default"].LOCATION, "localhost:11211");
    assert_eq!(caches["default"].TIMEOUT, Some(111));
}

#[test]
#[serial]
fn test_memcachier_env_vars_set() {
    clean_env();
    std::env::set_var("MEMCACHIER_PASSWORD", "pw");
    std::env::set_var("MEMCACHIER_SERVERS", "host1,host2");
    std::env::set_var("MEMCACHIER_USERNAME", "user");
    let caches = memcacheify_with_timeout(123);
    assert_eq!(caches["default"].LOCATION, "host1;host2");
    assert_eq!(caches["default"].TIMEOUT, Some(123));
    assert_eq!(std::env::var("MEMCACHE_SERVERS").unwrap(), "host1;host2");
    assert_eq!(std::env::var("MEMCACHE_USERNAME").unwrap(), "user");
    assert_eq!(std::env::var("MEMCACHE_PASSWORD").unwrap(), "pw");
    assert_eq!(caches["default"].BACKEND, "django_pylibmc.memcached.PyLibMCCache");
}

#[test]
#[serial]
fn test_memcachedcloud_env_vars_set() {
    clean_env();
    std::env::set_var("MEMCACHEDCLOUD_PASSWORD", "pwcloud");
    std::env::set_var("MEMCACHEDCLOUD_SERVERS", "c1,c2");
    std::env::set_var("MEMCACHEDCLOUD_USERNAME", "clouduser");
    let caches = memcacheify_with_timeout(321);
    assert_eq!(caches["default"].LOCATION, "c1;c2");
    assert_eq!(caches["default"].TIMEOUT, Some(321));
    assert_eq!(std::env::var("MEMCACHE_SERVERS").unwrap(), "c1;c2");
    assert_eq!(std::env::var("MEMCACHE_USERNAME").unwrap(), "clouduser");
    assert_eq!(std::env::var("MEMCACHE_PASSWORD").unwrap(), "pwcloud");
    assert_eq!(caches["default"].BACKEND, "django_pylibmc.memcached.PyLibMCCache");
}

#[test]
#[serial]
fn test_memcacheify_use_local() {
    clean_env();
    std::env::set_var("MEMCACHEIFY_USE_LOCAL", "1");
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django_pylibmc.memcached.PyLibMCCache");
}

#[test]
#[serial]
fn test_memcachier_incomplete_two_missing() {
    clean_env();
    std::env::set_var("MEMCACHIER_PASSWORD", "pw");
    std::env::set_var("MEMCACHIER_SERVERS", "h1");
    std::env::set_var("MEMCACHIER_USERNAME", "u1");
    std::env::remove_var("MEMCACHIER_PASSWORD");
    std::env::remove_var("MEMCACHIER_SERVERS");
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django.core.cache.backends.locmem.LocMemCache");
}

#[test]
#[serial]
fn test_memcachier_incomplete_one_missing() {
    clean_env();
    std::env::set_var("MEMCACHIER_PASSWORD", "pw");
    std::env::set_var("MEMCACHIER_SERVERS", "h1");
    std::env::set_var("MEMCACHIER_USERNAME", "u1");
    std::env::remove_var("MEMCACHIER_PASSWORD");
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django.core.cache.backends.locmem.LocMemCache");
}

#[test]
#[serial]
fn test_memcachedcloud_incomplete_two_missing() {
    clean_env();
    std::env::set_var("MEMCACHEDCLOUD_PASSWORD", "pw");
    std::env::set_var("MEMCACHEDCLOUD_SERVERS", "h1");
    std::env::set_var("MEMCACHEDCLOUD_USERNAME", "u1");
    std::env::remove_var("MEMCACHEDCLOUD_PASSWORD");
    std::env::remove_var("MEMCACHEDCLOUD_SERVERS");
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django.core.cache.backends.locmem.LocMemCache");
}

#[test]
#[serial]
fn test_memcachedcloud_incomplete_one_missing() {
    clean_env();
    std::env::set_var("MEMCACHEDCLOUD_PASSWORD", "pw");
    std::env::set_var("MEMCACHEDCLOUD_SERVERS", "h1");
    std::env::set_var("MEMCACHEDCLOUD_USERNAME", "u1");
    std::env::remove_var("MEMCACHEDCLOUD_PASSWORD");
    let caches = memcacheify();
    assert_eq!(caches["default"].BACKEND, "django.core.cache.backends.locmem.LocMemCache");
}

#[test]
#[serial]
fn test_memcacheify_timeout_default() {
    clean_env();
    std::env::set_var("MEMCACHE_PASSWORD", "p");
    std::env::set_var("MEMCACHE_SERVERS", "h");
    std::env::set_var("MEMCACHE_USERNAME", "u");
    let caches = memcacheify();
    assert_eq!(caches["default"].TIMEOUT, Some(500));
}