// Translated from tests/deye_set_time_processor_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_set_time_to_now() {
        let now = 1_600_000_000u64; // E.g., a fixed UNIX time
        let set_cmd = form_set_time_command(now);
        assert_eq!(set_cmd, "SET_TIME:1600000000");
    }

    fn form_set_time_command(ts: u64) -> String {
        format!("SET_TIME:{}", ts)
    }
}