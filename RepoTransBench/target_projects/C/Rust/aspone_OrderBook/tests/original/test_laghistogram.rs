// Translated from TestLagHistogram.h (logic reconstructed from HTML/gcov file)

use std::io::Write;

struct LagHistogram {
    name: String,
    data: Vec<u64>,
    max_samples: usize,
}

impl LagHistogram {
    fn new(name: &str, max_samples: usize) -> Self {
        Self {
            name: name.to_string(),
            data: Vec::with_capacity(max_samples),
            max_samples,
        }
    }
    fn add(&mut self, value: u64) {
        if self.data.len() < self.max_samples {
            self.data.push(value);
        }
    }
    fn print(&self) {
        if self.data.is_empty() {
            println!("No valid samples for run.");
            return;
        }
        let mut sorted = self.data.clone();
        sorted.sort_unstable();

        let min = sorted.first().unwrap();
        let max = sorted.last().unwrap();
        let mean = (sorted.iter().sum::<u64>() as f64) / (sorted.len() as f64);

        print!("Histogram for {}: num samples = {}, min = {}, max = {}, mean = {:.2}", self.name, sorted.len(), min, max, mean);

        if sorted.len() >= 11 {
            let p95 = sorted[(sorted.len() as f64 * 0.95) as usize - 1];
            let p99 = sorted[(sorted.len() as f64 * 0.99) as usize - 1];
            print!(", 95th = {}, 99th = {}", p95, p99);
        }
        if sorted.len() >= 10001 {
            let p9999 = sorted[(sorted.len() as f64 * 0.9999) as usize - 1];
            print!(", 99.99th = {}", p9999);
        }
        println!();
    }
}

#[test]
fn test_laghistogram_basic() {
    let mut hist = LagHistogram::new("Test", 5);
    hist.add(100);
    hist.add(30);
    hist.add(20);
    hist.add(70);
    hist.add(50);

    // Test print with >0 samples (should show statistics)
    hist.print();

    let hist2 = LagHistogram::new("Empty", 5);
    hist2.print(); // Should show "No valid samples for run."
}

#[test]
fn test_laghistogram_percentiles() {
    let mut hist = LagHistogram::new("Percentiles", 12);
    for i in 0..11 {
        hist.add(i * 10);
    }
    hist.print(); // Should print percentiles

    let mut hist3 = LagHistogram::new("BigHist", 105);
    for i in 0..101 {
        hist3.add(i * 10);
    }
    hist3.print(); // Should print 95th/99th

    let mut hist4 = LagHistogram::new("VeryBig", 10010);
    for i in 0..10000 {
        hist4.add(i);
    }
    hist4.print(); // Should print 99.99th
}