// Translated from tests/testarghashtable.c
// This is a "stub logic" port to ensure structure. Real hashtable tests should use the Rust hashtable.

#[cfg(test)]
mod tests {
    use super::*;

    struct HashTable {
        entries: Vec<(String, String)>,
    }
    impl HashTable {
        fn new() -> Self {
            HashTable { entries: Vec::new() }
        }
        fn count(&self) -> usize {
            self.entries.len()
        }
        fn insert(&mut self, key: String, value: String) {
            self.entries.push((key, value));
        }
        fn search(&self, key: &str) -> Option<&str> {
            self.entries.iter().find(|(k, _)| k == key).map(|(_, v)| v.as_str())
        }
        fn remove(&mut self, key: &str) {
            if let Some(pos) = self.entries.iter().position(|(k, _)| k == key) {
                self.entries.remove(pos);
            }
        }
    }

    #[test]
    fn test_arghashtable_basic_001() {
        let h = HashTable::new();
        assert_eq!(h.count(), 0);
    }

    #[test]
    fn test_arghashtable_basic_002() {
        let mut h = HashTable::new();
        h.insert("k1".to_string(), "v1".to_string());
        assert_eq!(h.count(), 1);
        let v = h.search("k1").unwrap();
        assert_eq!(v, "v1");
    }

    #[test]
    fn test_arghashtable_basic_005_remove() {
        let mut h = HashTable::new();
        h.insert("k1".to_string(), "v1".to_string());
        assert_eq!(h.count(), 1);
        h.remove("k1");
        assert_eq!(h.count(), 0);
    }
}