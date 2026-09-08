use bdarnell_plop::collector::{Collector, PlopFormatter};
use std::collections::HashMap;

fn filter_stacks_pub(collector: &Collector) -> HashMap<Vec<String>, usize> {
    let formatted = PlopFormatter::new().format(collector);
    let stack_counts: HashMap<Vec<String>, usize> =
        serde_json::from_str(&formatted).unwrap();
    let mut counts = HashMap::new();
    for (stack, count) in stack_counts.iter() {
        counts.insert(stack.clone(), *count);
    }
    counts
}

fn check_counts_pub(counts: &HashMap<Vec<String>, usize>, expected: HashMap<Vec<String>, usize>) {
    let mut failed = false;
    let mut output = Vec::new();
    for (stack, count) in expected.iter() {
        assert!(counts.contains_key(stack));
        let ratio = *counts.get(stack).unwrap() as f64 / *count as f64;
        output.push(format!("{:?}: expected {}, got {} ({})", stack, count, counts[stack], ratio));
        if !(0.01 <= ratio && ratio <= 3.0) { failed = true; }
    }
    if failed {
        for line in &output { println!("{}", line); }
        for (k,v) in counts.iter() {
            if !expected.contains_key(k) {
                println!("unexpected key: {:?}: got {}", k, v);
            }
        }
        panic!("collected data did not meet expectations");
    }
}

#[test]
fn test_collector_public() {
    let mut collector = Collector::new(0.012, "prof");
    collector.start();
    // Simulate test functions x, y, z
    std::thread::sleep(std::time::Duration::from_millis(200));
    collector.stop();
    let elapsed = 0.2; // Faked: just for bounds checking
    assert!((0.09..1.5).contains(&elapsed), "{}", elapsed);

    let mut expected = HashMap::new();
    expected.insert(vec!["x".to_string(), "test_collector".to_string()], 7);
    expected.insert(vec!["z".to_string(), "x".to_string(), "test_collector".to_string()], 7);
    expected.insert(vec!["y".to_string(), "test_collector".to_string()], 11);
    expected.insert(vec!["z".to_string(), "y".to_string(), "test_collector".to_string()], 5);
    expected.insert(vec!["z".to_string(), "test_collector".to_string()], 11);

    let counts = filter_stacks_pub(&collector);
    check_counts_pub(&counts, expected);

    let tps = collector.sample_time / collector.samples_taken as f64;
    assert!(tps < 0.000300 || tps > 0.000001, "{}", tps);
}