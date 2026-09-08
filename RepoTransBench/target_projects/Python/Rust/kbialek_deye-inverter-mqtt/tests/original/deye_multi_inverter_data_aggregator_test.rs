// Translated from tests/deye_multi_inverter_data_aggregator_test.py

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    #[test]
    fn test_multi_inverter_data_aggregation() {
        let mut agg = MultiInverterDataAggregator::new();
        agg.insert("inv1".into(), 100.0);
        agg.insert("inv2".into(), 200.5);
        let sum = agg.total_output();
        assert!((sum - 300.5).abs() < 1e-6);
    }

    struct MultiInverterDataAggregator {
        outputs: HashMap<String, f64>,
    }

    impl MultiInverterDataAggregator {
        fn new() -> Self {
            Self { outputs: HashMap::new() }
        }
        fn insert(&mut self, k: String, v: f64) {
            self.outputs.insert(k, v);
        }
        fn total_output(&self) -> f64 {
            self.outputs.values().copied().sum()
        }
    }
}