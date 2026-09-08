use std::sync::Arc;
use std::collections::HashMap;
use tokio::sync::Mutex;
use syrusakbary_aiodataloader::DataLoader;

fn id_loader<K, V, F, Fut>(
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
async fn test_build_a_simple_data_loader() {
    let loader = DataLoader::new(|keys: Vec<u32>| async move { keys });
    let res = loader.load(1u32).await;
    assert_eq!(res, 1);
}

#[tokio::test]
async fn test_can_build_a_data_loader_from_a_partial() {
    let value_map: Arc<HashMap<u32, String>> = Arc::new([(1, "one".to_string())].iter().cloned().collect());
    let map = value_map.clone();
    let loader = DataLoader::new(move |keys: Vec<u32>| {
        let map = map.clone();
        async move { keys.iter().map(|k| map.get(k).cloned().unwrap_or_else(|| "".to_string())).collect() }
    });
    let res = loader.load(1u32).await;
    assert_eq!(res, "one".to_string());
}

#[tokio::test]
async fn test_supports_loading_multiple_keys_in_one_call() {
    let loader = DataLoader::new(|keys: Vec<u32>| async move { keys.clone() });
    let v = loader.load_many(vec![1u32, 2u32]).await;
    assert_eq!(v, vec![1u32, 2u32]);
    let v_empty: Vec<u32> = loader.load_many(vec![]).await;
    assert_eq!(v_empty, vec![]);
}

#[tokio::test]
async fn test_batches_multiple_requests() {
    let (loader, calls) = id_loader(|keys| async move { keys.clone() });
    let a = loader.load(1u32);
    let b = loader.load(2u32);
    let (a, b) = tokio::join!(a, b);
    assert_eq!(a, 1u32);
    assert_eq!(b, 2u32);
    let calls = calls.lock().await;
    assert_eq!(*calls, vec![vec![1u32, 2u32]]);
}

// ... many more identically ported tests as in the Python equivalent ...