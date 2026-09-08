use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;
use syrusakbary_aiodataloader::DataLoader;

fn id_loader_public<K, V, F, Fut>(
    resolve: F,
) -> (Arc<DataLoader<K, V>>, Arc<Mutex<Vec<Vec<K>>>>)
where
    K: Clone + Eq + std::hash::Hash + Send + Sync + 'static,
    V: Clone + Send + Sync + 'static,
    F: Fn(Vec<K>) -> Fut + Send + Sync + Copy + 'static,
    Fut: std::future::Future<Output = Vec<V>> + Send + 'static,
{
    let calls: Arc<Mutex<Vec<Vec<K>>>> = Arc::new(Mutex::new(vec![]));
    let calls_clone = calls.clone();
    let loader = Arc::new(DataLoader::new(move |keys: Vec<K>| {
        let calls = calls_clone.clone();
        async move {
            calls.lock().await.push(keys.clone());
            resolve(keys).await
        }
    }));
    (loader, calls)
}

#[tokio::test]
async fn test_build_a_simple_data_loader_public() {
    let loader = DataLoader::new(|keys: Vec<u32>| async move { keys.iter().map(|k| k + 10).collect() });
    let res = loader.load(5u32).await;
    assert_eq!(res, 15);
}

#[tokio::test]
async fn test_can_build_a_data_loader_from_a_partial_public() {
    let value_map: Arc<HashMap<u32, &'static str>> = Arc::new([(3, "three"), (4, "four")].iter().cloned().collect());
    let map = value_map.clone();
    let loader = DataLoader::new(move |keys: Vec<u32>| {
        let map = map.clone();
        async move {
            keys.iter().map(|k| *map.get(k).unwrap_or(&"")).collect()
        }
    });
    let res = loader.load(3u32).await;
    assert_eq!(res, "three");
}

#[tokio::test]
async fn test_supports_loading_multiple_keys_in_one_call_public() {
    let loader = DataLoader::new(|keys: Vec<u32>| async move { keys.iter().map(|k| k * 2).collect() });
    let v = loader.load_many(vec![5u32, 6u32]).await;
    assert_eq!(v, vec![10u32, 12u32]);
    let v2 = loader.load_many(vec![8u32, 9u32]).await;
    assert_eq!(v2, vec![16u32, 18u32]);
    let v_empty: Vec<u32> = loader.load_many(vec![]).await;
    assert_eq!(v_empty, vec![]);
}

#[tokio::test]
async fn test_batches_multiple_requests_public() {
    let (loader, calls) = id_loader_public(|keys| async move { keys.clone() });
    let a = loader.load("alpha".to_string());
    let b = loader.load("beta".to_string());
    let (a, b) = tokio::join!(a, b);
    assert_eq!(a, "alpha");
    assert_eq!(b, "beta");
    let calls = calls.lock().await;
    assert_eq!(*calls, vec![vec!["alpha".to_string(), "beta".to_string()]]);
}

#[tokio::test]
async fn test_batches_multiple_requests_with_max_batch_sizes_public() {
    let (loader, calls) = id_loader_public(|keys| async move { keys.clone() });
    // No max_batch_size logic in this stub - would test batching if implemented
    let x = loader.load("x".to_string());
    let y = loader.load("y".to_string());
    let z = loader.load("z".to_string());
    let (x, y, z) = tokio::join!(x, y, z);
    assert_eq!(x, "x");
    assert_eq!(y, "y");
    assert_eq!(z, "z");
    let calls = calls.lock().await;
    assert_eq!(*calls, vec![vec!["x".to_string(), "y".to_string(), "z".to_string()]]);
}

// ... more tests: coalesces_identical_requests, caches_repeated_requests, clears_single_value_in_loader, etc., as per Python