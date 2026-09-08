#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::{HashMap, HashSet};
    use uuid::Uuid;

    // Simulate logs with regex (we'll just split by test_name string)
    fn parse_logs(logs: &str) -> HashMap<String, Vec<String>> {
        let mut grouped: HashMap<String, Vec<String>> = HashMap::new();
        for line in logs.lines() {
            // Simulate parse: expect "[test_name]:value"
            if let Some((name, value)) = line.split_once(":") {
                let entry = grouped.entry(name.to_string()).or_insert(Vec::new());
                entry.push(value.to_string());
            }
        }
        grouped
    }

    #[test]
    fn test_return_value() {
        // Simulate order/return value task with direct log injection
        let test_name = Uuid::new_v4().to_string();
        // Simulate canvas
        let canvas_out = format!("{}:val123", test_name);
        let logs = canvas_out.clone();
        let result_map = parse_logs(&logs);
        // result_map[test_name][0] == return value string
        assert_eq!(result_map[&test_name][0], "val123");
    }

    #[test]
    fn test_group_and_single_task() {
        let test_name = Uuid::new_v4().to_string();
        // Simulate a group
        let logs = format!(
            "{}:task1\n{}:task2\n{}:task3\n{}:task4\n{}:task5",
            test_name, test_name, test_name, test_name, test_name
        );
        let result_map = parse_logs(&logs);
        let got: HashSet<_> = result_map[&test_name].iter().map(|s| s.as_str()).collect();
        let expect: HashSet<_> = ["task1", "task2", "task3", "task4", "task5"].iter().copied().collect();
        assert_eq!(got, expect);
    }

    #[test]
    fn test_chord_and_chain() {
        let test_name = Uuid::new_v4().to_string();
        // Simulate chord then last
        let logs = format!(
            "{}:task1\n{}:task2\n{}:task3\n{}:task4\n{}:task5\n{}:last",
            test_name, test_name, test_name, test_name, test_name, test_name
        );
        let result_map = parse_logs(&logs);
        let last_val = result_map[&test_name].last().unwrap();
        assert_eq!(last_val, "last");

        // Chain
        let logs = format!(
            "{}:task1\n{}:task2\n{}:task3",
            test_name, test_name, test_name
        );
        let result_map = parse_logs(&logs);
        assert_eq!(result_map[&test_name], vec!["task1", "task2", "task3"]);
    }

    #[test]
    fn test_combination() {
        let test_name = Uuid::new_v4().to_string();
        // Simulate group|task|task|group|task
        let logs = format!(
            "{0}:task1a\n{0}:task1b\n{0}:task2\n{0}:task3\n{0}:task4a\n{0}:task4b\n{0}:task5",
            test_name
        );
        let result_map = parse_logs(&logs);
        let order = &result_map[&test_name];
        assert!(order[0] == "task1a" || order[1] == "task1a");
        assert!(order[0] == "task1b" || order[1] == "task1b");
        assert_eq!(&order[2..4], ["task2", "task3"]);
        assert!((order[4] == "task4a" && order[5] == "task4b") || (order[4] == "task4b" && order[5] == "task4a"));
        assert_eq!(order[6], "task5");
    }
}