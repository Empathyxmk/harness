// Translated from tests/test_records_additional.py

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
struct PersonRecord {
    name: String,
}

struct RecordCollection<T: Clone + PartialEq> {
    collection: Vec<T>,
}

impl<T: Clone + PartialEq> RecordCollection<T> {
    fn new<I: Iterator<Item = T>>(iter: I) -> Self {
        Self { collection: iter.collect() }
    }

    fn filter<F>(&self, mut func: F) -> Vec<T>
    where
        F: FnMut(&T) -> bool,
    {
        self.collection.iter().cloned().filter(|x| func(x)).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_collection_filter_example() {
        let names = vec!["a", "b", "c"];
        let rows = RecordCollection::new(names.iter().map(|name| PersonRecord { name: name.to_string() }));
        let filtered: Vec<PersonRecord> = rows.filter(|rec| rec.name == "b");
        assert_eq!(filtered, vec![PersonRecord { name: "b".to_string() }]);
    }

    #[test]
    fn test_record_equality() {
        #[derive(Debug, Clone, PartialEq)]
        struct Record {
            fields: HashMap<String, String>,
        }

        impl Record {
            fn new(keys: &[&str], values: &[&str]) -> Self {
                let mut fields = HashMap::new();
                for (key, value) in keys.iter().zip(values.iter()) {
                    fields.insert(key.to_string(), value.to_string());
                }
                Record { fields }
            }
        }

        let keys = vec!["id", "name"];
        let values1 = vec!["1", "foo"];
        let values2 = vec!["1", "foo"];
        let r1 = Record::new(&keys, &values1);
        let r2 = Record::new(&keys, &values2);
        assert_eq!(r1, r2);

        let values3 = vec!["2", "foo"];
        let r3 = Record::new(&keys, &values3);
        assert_ne!(r1, r3);
    }

    #[test]
    fn test_record_repr_debug() {
        #[derive(Debug, Clone, PartialEq)]
        struct Record {
            fields: HashMap<String, String>,
        }

        impl Record {
            fn new(keys: &[&str], values: &[&str]) -> Self {
                let mut fields = HashMap::new();
                for (key, value) in keys.iter().zip(values.iter()) {
                    fields.insert(key.to_string(), value.to_string());
                }
                Record { fields }
            }
        }

        let keys = vec!["id", "name"];
        let values = vec!["1", "foo"];
        let r = Record::new(&keys, &values);
        let s = format!("{:?}", r);
        assert!(s.contains("fields"));
        assert!(s.contains("id"));
        assert!(s.contains("name"));
        assert!(s.contains("foo"));
    }
}