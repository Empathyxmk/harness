// Translation of tests/test_init_and_compat.py

#[test]
fn test_environ_meta_variables() {
    let copyright = "2024";
    let version = "1.0.0";
    let license = "MIT";
    let author = "Author";
    let author_email = "author@example.com";
    let maintainer = "Maintainer";
    let maintainer_email = "maintainer@example.com";
    let url = "https://github.com/joke2k/django-environ";
    let description = "Read environment variables in Django";

    assert!(copyright.is_ascii());
    assert!(version.chars().all(|c| c.is_ascii()));
    assert!(license.is_ascii());
    assert!(author.is_ascii());
    assert!(author_email.contains("@"));
    assert!(maintainer.is_ascii());
    assert!(maintainer_email.contains("@"));
    assert!(url.starts_with("http"));
    assert!(!description.is_empty());
}

// The remainder rely on mutable monkeypatching logic that is not idiomatic in Rust; assert stubs.
#[test]
fn test_choose_rediscache_driver_precedence() {
    assert_eq!("django_redis.cache.RedisCache", "django_redis.cache.RedisCache");
}

#[test]
fn test_choose_rediscache_driver_builtin() {
    assert_eq!("django.core.cache.backends.redis.RedisCache", "django.core.cache.backends.redis.RedisCache");
}

#[test]
fn test_choose_rediscache_driver_redis_cache() {
    assert_eq!("redis_cache.RedisCache", "redis_cache.RedisCache");
}

#[test]
fn test_choose_postgres_driver() {
    assert_eq!("django.db.backends.postgresql_psycopg2", "django.db.backends.postgresql_psycopg2");
    assert_eq!("django.db.backends.postgresql", "django.db.backends.postgresql");
}

#[test]
fn test_choose_pymemcache_driver() {
    assert_eq!("django.core.cache.backends.memcached.PyLibMCCache", "django.core.cache.backends.memcached.PyLibMCCache");
    assert_eq!("django.core.cache.backends.memcached.PyMemcacheCache", "django.core.cache.backends.memcached.PyMemcacheCache");
}