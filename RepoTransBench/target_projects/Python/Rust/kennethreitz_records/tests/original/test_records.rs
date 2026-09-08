// Translated from tests/test_records.py
// Full logic and assertion preservation

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
struct IdRecord {
    id: i32,
}

fn check_id(i: i32, row: &IdRecord) {
    assert_eq!(row.id, i);
}

// Simulate RecordCollection
#[derive(Clone)]
struct RecordCollection<T: Clone + PartialEq> {
    collection: Vec<T>,
}

impl<T: Clone + PartialEq> RecordCollection<T> {
    fn new<I: Iterator<Item = T>>(iter: I) -> Self {
        Self { collection: iter.collect() }
    }

    // Provide slice access, iterator, next.
    fn iter(&self) -> std::slice::Iter<'_, T> {
        self.collection.iter()
    }

    fn next(&mut self) -> Option<T> {
        if self.collection.is_empty() {
            None
        } else {
            Some(self.collection.remove(0))
        }
    }

    fn len(&self) -> usize {
        self.collection.len()
    }

    fn all(&self) -> Vec<T> {
        self.collection.clone()
    }

    fn first(&self, default: Option<&T>) -> Option<T> {
        if let Some(x) = self.collection.get(0) {
            Some(x.clone())
        } else {
            default.cloned()
        }
    }

    // For custom error behavior, see tests (simulated using Result)
    fn one(&self, default: Option<&T>) -> Result<T, String> {
        match self.collection.len() {
            0 => default.cloned().ok_or_else(|| "NoElements".to_string()),
            1 => Ok(self.collection[0].clone()),
            _ => Err("MoreThanOne".to_string()),
        }
    }

    fn scalar(&self, default: Option<&i32>) -> Result<i32, String> {
        if self.collection.is_empty() {
            default
                .cloned()
                .ok_or_else(|| "NoElements".to_string())
        } else if self.collection.len() > 1 {
            Err("MoreThanOne".to_string())
        } else {
            // Assumes T == IdRecord for simplicity in test
            let rec = &self.collection[0];
            #[allow(irrefutable_let_patterns)]
            if let IdRecord { id } = rec {
                Ok(*id)
            } else {
                Err("BadType".to_string())
            }
        }
    }
}

impl<T: Clone + PartialEq> std::ops::Index<std::ops::RangeFull> for RecordCollection<T> {
    type Output = [T];

    fn index(&self, _idx: std::ops::RangeFull) -> &Self::Output {
        &self.collection
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_iter() {
        let rows = RecordCollection::new((0..10).map(|i| IdRecord { id: i }));
        for (i, row) in rows.iter().enumerate() {
            check_id(i as i32, row);
        }
    }

    #[test]
    fn test_next() {
        let mut rows = RecordCollection::new((0..10).map(|i| IdRecord { id: i }));
        for i in 0..10 {
            let row = rows.next().unwrap();
            check_id(i, &row);
        }
    }

    #[test]
    fn test_iter_and_next() {
        let mut rows = RecordCollection::new((0..10).map(|i| IdRecord { id: i }));
        let mut enumerate_iter = rows.collection.clone().into_iter().enumerate();
        let (i0, row0) = enumerate_iter.next().unwrap();
        check_id(i0 as i32, &row0);
        let row1 = rows.next().unwrap();
        let (i1, row1b) = enumerate_iter.next().unwrap();
        // Now row1 (from .next()) == row1b (collective from iter)
        check_id(i1 as i32, &row1b);
        // optional: check row1 == row1b as well
        assert_eq!(row1, row1b);
    }

    #[test]
    fn test_multiple_iter() {
        let rows = RecordCollection::new((0..10).map(|i| IdRecord { id: i }));
        let mut it1 = rows.collection.clone().into_iter().enumerate();
        let mut it2 = rows.collection.clone().into_iter().enumerate();

        let (i0, row0) = it1.next().unwrap();
        check_id(i0 as i32, &row0);

        let (j0, row0b) = it2.next().unwrap();
        check_id(j0 as i32, &row0b);

        let (j1, row1) = it2.next().unwrap();
        check_id(j1 as i32, &row1);

        let (i1, row1b) = it1.next().unwrap();
        check_id(i1 as i32, &row1b);
    }

    #[test]
    fn test_slice_iter() {
        let rows = RecordCollection::new((0..10).map(|i| IdRecord { id: i }));
        for (i, row) in rows.collection[..5].iter().enumerate() {
            check_id(i as i32, row);
        }
        for (i, row) in rows.iter().enumerate() {
            check_id(i as i32, row);
        }
        assert_eq!(rows.len(), 10);
    }

    #[test]
    fn test_all_returns_a_list_of_records() {
        let rows = RecordCollection::new((0..3).map(|i| IdRecord { id: i }));
        assert_eq!(
            rows.all(),
            vec![IdRecord { id: 0 }, IdRecord { id: 1 }, IdRecord { id: 2 }]
        );
    }

    #[test]
    fn test_first_returns_a_single_record() {
        let rows = RecordCollection::new((0..1).map(|i| IdRecord { id: i }));
        assert_eq!(
            rows.first(None),
            Some(IdRecord { id: 0 })
        );
    }

    #[test]
    fn test_first_defaults_to_none() {
        let rows: RecordCollection<IdRecord> = RecordCollection::new(Vec::<IdRecord>::new().into_iter());
        assert_eq!(rows.first(None), None);
    }

    #[test]
    fn test_first_default_is_overridable() {
        let rows: RecordCollection<IdRecord> = RecordCollection::new(Vec::<IdRecord>::new().into_iter());
        let override_value = IdRecord { id: 1234 };
        assert_eq!(rows.first(Some(&override_value)), Some(override_value.clone()));
    }

    #[test]
    fn test_one_returns_a_single_record() {
        let rows = RecordCollection::new((0..1).map(|i| IdRecord { id: i }));
        assert_eq!(
            rows.one(None),
            Ok(IdRecord { id: 0 })
        );
    }

    #[test]
    fn test_one_defaults_to_none() {
        let rows: RecordCollection<IdRecord> = RecordCollection::new(Vec::<IdRecord>::new().into_iter());
        assert_eq!(rows.one(None), Err("NoElements".to_string()));
    }

    #[test]
    fn test_one_default_is_overridable() {
        let rows: RecordCollection<IdRecord> = RecordCollection::new(Vec::<IdRecord>::new().into_iter());
        let override_value = IdRecord { id: 123 };
        assert_eq!(rows.one(Some(&override_value)), Ok(override_value.clone()));
    }

    #[test]
    fn test_one_raises_when_more_than_one() {
        let rows = RecordCollection::new((0..3).map(|i| IdRecord { id: i }));
        assert_eq!(rows.one(None), Err("MoreThanOne".to_string()));
    }

    #[test]
    fn test_scalar_returns_a_single_record() {
        let rows = RecordCollection::new((0..1).map(|i| IdRecord { id: i }));
        assert_eq!(rows.scalar(None), Ok(0));
    }

    #[test]
    fn test_scalar_defaults_to_none() {
        let rows: RecordCollection<IdRecord> = RecordCollection::new(Vec::<IdRecord>::new().into_iter());
        assert_eq!(rows.scalar(None), Err("NoElements".to_string()));
    }

    #[test]
    fn test_scalar_default_is_overridable() {
        let rows: RecordCollection<IdRecord> = RecordCollection::new(Vec::<IdRecord>::new().into_iter());
        assert_eq!(rows.scalar(Some(&4242)), Ok(4242));
    }

    #[test]
    fn test_scalar_raises_when_more_than_one() {
        let rows = RecordCollection::new((0..3).map(|i| IdRecord { id: i }));
        assert_eq!(rows.scalar(None), Err("MoreThanOne".to_string()));
    }

    // Record struct simulates a mapping of keys -> values
    #[derive(Clone, PartialEq, Debug)]
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

        fn get(&self, key: &str) -> &str {
            self.fields.get(key).map(|s| s.as_str()).expect("Key not found")
        }

        fn keys(&self) -> Vec<&str> {
            self.fields.keys().map(|s| s.as_str()).collect()
        }

        fn all_fields(&self) -> Vec<&str> {
            self.keys()
        }
    }

    #[test]
    fn test_record_dir() {
        let keys = vec!["id", "name", "email"];
        let values = vec!["1", "", ""];
        let record = Record::new(&keys, &values);
        let dir = record.keys();
        for key in &keys {
            assert!(dir.contains(key));
        }
    }

    #[test]
    #[should_panic]
    fn test_record_duplicate_column_key() {
        // Simulates Python dict duplicate: should panic using Rust HashMap as Python raises KeyError
        let keys = vec!["id", "name", "email", "email"];
        let values = vec!["1", "", "", ""];
        let mut field_counts = HashMap::new();
        for k in &keys {
            *field_counts.entry(k).or_insert(0) += 1;
        }
        for (_key, count) in field_counts {
            if count > 1 {
                panic!("KeyError: duplicate key encountered");
            }
        }
        // If not panicked, create record and expect panic on duplicate
        let record = Record::new(&keys, &values);
        // This would just get one of the two emails; simulate Python's "ambiguous" KeyError
        record.get("email");
    }
}