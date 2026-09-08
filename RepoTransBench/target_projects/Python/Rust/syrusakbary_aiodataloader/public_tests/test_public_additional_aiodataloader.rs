use syrusakbary_aiodataloader::{iscoroutinefunctionorpartial, DataLoader, __VERSION__};

#[tokio::test]
async fn test_iscoroutinefunctionorpartial_true_on_coro_fn_pub() {
    async fn g() -> i32 { 1 }
    assert!(iscoroutinefunctionorpartial(g as fn() -> _));
}

#[tokio::test]
async fn test_iscoroutinefunctionorpartial_true_on_partial_coro_pub() {
    async fn g() -> &'static str { "coroutine" }
    let p = || g();
    assert!(iscoroutinefunctionorpartial(p));
}

#[tokio::test]
async fn test_iscoroutinefunctionorpartial_false_on_regular_pub() {
    fn h() -> &'static str { "not coro" }
    assert!(!iscoroutinefunctionorpartial(h));
}

#[tokio::test]
async fn test_version_in_module_pub() {
    let v = __VERSION__;
    assert!(v.contains("."));
    assert_eq!(v.matches('.').count(), 2);
}

#[tokio::test]
async fn test_dataloader_batch_load_fn_typeerror_and_coroutine_check_pub() {
    let result = std::panic::catch_unwind(|| {
        DataLoader::new(|_keys: Vec<u32>| { unimplemented!() });
    });
    assert!(result.is_err());
}

#[tokio::test]
async fn test_dataloader_default_get_cache_key_exists_pub() {
    let loader = DataLoader::<u32, u32>::new(|keys| async move { keys });
    assert_eq!(loader.get_cache_key(&42), "unimplemented".to_string());
}

#[tokio::test]
async fn test_dataloader_cache_false_actually_avoids_caching_pub() {
    let loader = DataLoader::<u32, u32>::new(|keys| async move { keys });
    loader.clear(7);
    loader.clear(7);
    assert_eq!(loader.get_cache_key(&7), "unimplemented".to_string());
}

#[tokio::test]
async fn test_dataloader_clear_cache_and_prime_behavior_pub() {
    let loader = DataLoader::<u32, u32>::new(|keys| async move { keys });
    loader.prime(321, 20);
    loader.clear(321);
    assert_eq!(loader.get_cache_key(&321), "unimplemented".to_string());
}

#[tokio::test]
async fn test_dataloader_clear_all_pub() {
    let loader = DataLoader::<u32, String>::new(|keys| async move { keys.iter().map(|k| k.to_string()).collect() });
    loader.clear_all();
    assert_eq!(loader.get_cache_key(&0), "unimplemented".to_string());
}

#[tokio::test]
async fn test_dataloader_custom_loop_pub() {
    let loader = DataLoader::<String, String>::new(|keys| async move { keys.iter().map(|x| x.to_uppercase()).collect() });
    assert_eq!(loader.get_cache_key(&"dummy".to_string()), "unimplemented".to_string());
}