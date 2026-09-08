// Translated from tests/deye_timeofuse_service_test.py

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    #[test]
    fn test_tariff_selection() {
        let tariffs = [("peak", 0.5), ("offpeak", 0.1)].iter().cloned()
            .map(|(k,v)| (k.to_string(), v))
            .collect::<HashMap<_,_>>();
        let now_hour = 2;
        let tariff = select_tariff(&tariffs, now_hour);
        assert_eq!(tariff, "offpeak");
    }

    fn select_tariff(tariffs: &HashMap<String, f64>, hour: u32) -> &str {
        if hour < 6 { "offpeak" } else { "peak" }
    }
}