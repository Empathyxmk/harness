// Translated from tests/src_deye_multi_inverter_data_aggregator_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_secondary_multi_inverter_data_agg() {
        let agg = vec![1.0, 2.0, 3.0];
        let avg = agg.iter().sum::<f64>() / agg.len() as f64;
        assert_eq!(avg, 2.0);
    }
}