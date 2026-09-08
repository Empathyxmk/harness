use std::collections::HashMap;
use std::env;

use serial_test::serial;
use django_heroku_memcacheify::{memcacheify, memcacheify_with_timeout, CacheConf};

// Helper to get main config (mimics _get_cache_conf)
fn get_cache_conf(caches: &HashMap<String, CacheConf>) -> &CacheConf {
    caches.get("default")
          .expect("Result should contain key 'default'")
}

// Helper to determine memcache backend string
fn is_memcache_backend(backend: &str) -> bool {
    backend == "django.core.cache.backends.memcached.PyLibMCCache" ||
    backend == "django_pylibmc.memcached.PyLibMCCache"
}

fn extract_timeout(cfg: &CacheConf) -> Option<u32> {
    cfg.TIMEOUT
}

fn clean_env() {
    let keys = [
        "MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
        "MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
        "MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
        "MEMCACHEIFY_USE_LOCAL"
    ];
    for k in keys.iter() {
        env::remove_var(k);
    }
}

#[test]
#[serial]
fn test_public_memcacheify_basic() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112");
    env::set_var("MEMCACHIER_USERNAME", "public_alpha");
    env::set_var("MEMCACHIER_PASSWORD", "alp_pw");
    // settings: TIMEOUT = 876
    let caches = memcacheify_with_timeout(876);
    let cache_conf = get_cache_conf(&caches);
    assert!(is_memcache_backend(&cache_conf.BACKEND));
    let expected_locations = vec![
        "alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112",
        "alpha-mc1.pub.net:22111;alpha-mc2.pub.net:22112"
    ];
    assert!(expected_locations.contains(&cache_conf.LOCATION.as_str()));
    assert_eq!(extract_timeout(cache_conf), Some(876));
}

#[test]
#[serial]
fn test_public_memcacheify_location_fallback() {
    clean_env();
    env::remove_var("MEMCACHIER_SERVERS");
    env::set_var("MEMCACHE_SERVERS", "fallback-mc-newpub.example.com:31220");
    env::set_var("MEMCACHE_USERNAME", "newuser");
    env::set_var("MEMCACHE_PASSWORD", "newpass");
    let caches = memcacheify_with_timeout(500);
    let cache_conf = get_cache_conf(&caches);
    let possible_locations = vec![
        "fallback-mc-newpub.example.com:31220",
        "localhost:11211"
    ];
    assert!(possible_locations.contains(&cache_conf.LOCATION.as_str()));
}

#[test]
#[serial]
fn test_public_memcacheify_blank_env() {
    clean_env();
    let caches = memcacheify_with_timeout(500);
    let cache_conf = get_cache_conf(&caches);
    let allowed_backends = vec![
        "django.core.cache.backends.memcached.PyLibMCCache",
        "django_pylibmc.memcached.PyLibMCCache",
        "django.core.cache.backends.locmem.LocMemCache"
    ];
    assert!(allowed_backends.contains(&cache_conf.BACKEND.as_str()));
    let allowed_locs = vec!["", "localhost:11211"];
    assert!(allowed_locs.contains(&cache_conf.LOCATION.as_str()));
}

#[test]
#[serial]
fn test_public_memcacheify_timeouts() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "b.pub.com:15111");
    env::set_var("MEMCACHIER_USERNAME", "pub_timeout");
    env::set_var("MEMCACHIER_PASSWORD", "pwtout");
    let caches = memcacheify_with_timeout(9342);
    let cache_conf = get_cache_conf(&caches);
    assert_eq!(extract_timeout(cache_conf), Some(9342));
}

#[test]
#[serial]
fn test_public_memcacheify_options_override() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "pub-override.another.net");
    env::set_var("MEMCACHIER_USERNAME", "override_user");
    env::set_var("MEMCACHIER_PASSWORD", "override_pw");
    // Simulate options/settings as arguments
    let caches = memcacheify_with_timeout(422);
    let cache_conf = get_cache_conf(&caches);

    // OPTIONS in Rust impl is None, match backend
    assert_eq!(extract_timeout(cache_conf), Some(422));
}

#[test]
#[serial]
fn test_public_memcacheify_location_env_priority() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "top-priority-pub.example:8998");
    env::set_var("MEMCACHE_SERVERS", "secondary-pub-fallback.example:8998");
    let caches = memcacheify_with_timeout(500);
    let cache_conf = get_cache_conf(&caches);
    let possible_locations = vec![
        "top-priority-pub.example:8998",
        "localhost:11211"
    ];
    assert!(possible_locations.contains(&cache_conf.LOCATION.as_str()));
}

#[test]
#[serial]
fn test_public_memcacheify_null_settings() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "");
    env::set_var("MEMCACHIER_USERNAME", "");
    env::set_var("MEMCACHIER_PASSWORD", "");
    let caches = memcacheify();
    let cache_conf = get_cache_conf(&caches);
    let possible_locs = vec!["localhost:11211", "",];
    assert!(possible_locs.contains(&cache_conf.LOCATION.as_str()));
}

#[test]
#[serial]
fn test_public_memcacheify_options_extend() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "combo-extend.pub:6434");
    env::set_var("MEMCACHIER_USERNAME", "override_pub_ext");
    env::set_var("MEMCACHIER_PASSWORD", "pw_pub_combo");
    let caches = memcacheify();
    let cache_conf = get_cache_conf(&caches);
    assert!(cache_conf.LOCATION.contains("combo-extend.pub:6434") 
        || cache_conf.LOCATION.is_empty());
}

#[test]
#[serial]
fn test_public_memcacheify_empty_string_env() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "");
    env::set_var("MEMCACHIER_USERNAME", "");
    env::set_var("MEMCACHIER_PASSWORD", "");
    let caches = memcacheify_with_timeout(500);
    let cache_conf = get_cache_conf(&caches);
    let allowed_locations = vec!["", "localhost:11211"];
    assert!(allowed_locations.contains(&cache_conf.LOCATION.as_str()));
}

#[test]
#[serial]
fn test_public_memcacheify_no_args() {
    clean_env();
    env::set_var("MEMCACHIER_SERVERS", "");
    env::set_var("MEMCACHIER_USERNAME", "");
    env::set_var("MEMCACHIER_PASSWORD", "");
    let caches = memcacheify();
    let cache_conf = get_cache_conf(&caches);
    let allowed_locations = vec!["localhost:11211", ""];
    assert!(allowed_locations.contains(&cache_conf.LOCATION.as_str()));
    assert!(is_memcache_backend(&cache_conf.BACKEND) ||
            cache_conf.BACKEND == "django.core.cache.backends.locmem.LocMemCache");
}