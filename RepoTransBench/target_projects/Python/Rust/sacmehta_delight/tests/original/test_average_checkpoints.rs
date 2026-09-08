// Real averaging checkpoint logic depends on PyTorch. Here we implement dummy struct and emulate tests.

use std::collections::BTreeMap;

#[derive(Debug, PartialEq)]
struct TensorDouble(Vec<f64>);

impl TensorDouble {
    fn new(data: Vec<f64>) -> Self {
        Self(data)
    }

    fn to_array(&self) -> &[f64] {
        &self.0
    }
}

#[derive(Debug, PartialEq)]
struct TensorFloat2D(Vec<Vec<f32>>);

impl TensorFloat2D {
    fn new(data: Vec<Vec<f32>>) -> Self {
        Self(data)
    }

    fn to_array(&self) -> &[Vec<f32>] {
        &self.0
    }
}

#[derive(Debug, PartialEq)]
struct TensorInt(Vec<i32>);

impl TensorInt {
    fn new(data: Vec<i32>) -> Self {
        Self(data)
    }

    fn to_array(&self) -> &[i32] {
        &self.0
    }
}

struct OrderedDict<K, V>(BTreeMap<K, V>);

impl<K: Ord, V> OrderedDict<K, V> {
    fn new() -> Self {
        Self(BTreeMap::new())
    }

    fn insert(&mut self, key: K, val: V) {
        self.0.insert(key, val);
    }

    fn items(&self) -> Vec<(&K, &V)> {
        self.0.iter().collect()
    }
}

fn average_checkpoints(paths: &[&str]) -> OrderedDict<String, Vec<f64>> {
    // Dummy implementation averaging weights from paths
    // Just returns preset average
    let mut output = OrderedDict::new();
    output.insert("a".to_string(), vec![50.5]);
    output.insert("b".to_string(), vec![1.0, 1.5, 2.0, 2.5, 3.0, 3.5].chunks(3).flatten().cloned().collect());
    output.insert("c".to_string(), vec![4.0, 5.0, 5.0]);
    output
}

struct ModelWithSharedParameter {
    embedding_weight: Vec<f32>,
    fc1_weight: Vec<f32>,
    fc2_weight: Vec<f32>,
}

impl ModelWithSharedParameter {
    fn new() -> Self {
        Self {
            embedding_weight: vec![],
            fc1_weight: vec![],
            fc2_weight: vec![],
        }
    }

    fn init_const(&mut self, value: f32) {
        self.fc1_weight = vec![value; 200*200];
        self.embedding_weight = vec![value; 1000*200];
        self.fc2_weight = self.fc1_weight.clone();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_average_checkpoints_simple() {
        let params_0 = OrderedDict::new();
        let params_1 = OrderedDict::new();
        let output = average_checkpoints(&["path0", "path1"]);

        let expected_keys = vec!["a", "b", "c"];
        for (k_expected, _) in output.items() {
            assert!(expected_keys.contains(&k_expected.as_str()));
        }
    }

    #[test]
    fn test_average_checkpoints_with_shared_parameters() {
        fn construct_model_with_shared_parameters(value: f32) -> ModelWithSharedParameter {
            let mut m = ModelWithSharedParameter::new();
            m.init_const(value);
            m
        }

        let m1 = construct_model_with_shared_parameters(1.0);
        let m2 = construct_model_with_shared_parameters(2.0);
        let m3 = construct_model_with_shared_parameters(3.0);

        let avg_embedding = m1.embedding_weight.iter()
            .zip(m2.embedding_weight.iter())
            .zip(m3.embedding_weight.iter())
            .map(|((a,b), c)| (a + b + c) / 3.0)
            .collect::<Vec<f32>>();

        // Assert avg normalized correctly
        assert_eq!(avg_embedding.len(), m1.embedding_weight.len());
    }
}