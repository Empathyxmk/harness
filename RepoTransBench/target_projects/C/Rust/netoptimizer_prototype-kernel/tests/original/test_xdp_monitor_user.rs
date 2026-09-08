use std::ffi::CStr;
use std::ffi::CString;
use std::os::raw::c_char;

type __u64 = u64;

const REDIR_SUCCESS: usize = 0;
const REDIR_ERROR: usize = 1;
const REDIR_RES_MAX: usize = 2;

static REDIR_NAMES: [&'static str; REDIR_RES_MAX] = [
    "Success",
    "Error",
];

fn err2str(err: i32) -> Option<&'static str> {
    if err >= 0 && (err as usize) < REDIR_RES_MAX {
        Some(REDIR_NAMES[err as usize])
    } else {
        None
    }
}

fn cstrcmp(a: &str, b: &str) -> i32 {
    // Simulate C strcmp: 0 if equal, nonzero otherwise
    if a == b { 0 } else { 1 }
}

#[test]
fn test_err2str() {
    assert_eq!(cstrcmp(err2str(REDIR_SUCCESS as i32).unwrap(), "Success"), 0);
    assert_eq!(cstrcmp(err2str(REDIR_ERROR as i32).unwrap(), "Error"), 0);
    assert!(err2str(-1).is_none());
    assert!(err2str(100).is_none());
}

#[derive(Clone, Copy, Debug, Default)]
struct Record {
    counter: __u64,
    timestamp: __u64,
}

#[derive(Clone, Copy, Debug, Default)]
struct StatsRecord {
    xdp_redir: [Record; REDIR_RES_MAX],
}

fn stats_print_headers(err_only: bool) {
    if err_only {
        println!(
            "\nNOTICE: Only tracking XDP redirect errors\n         Enable TX success stats via '--stats'\n         (which comes with a per packet processing overhead)\n"
        );
    }

    println!(
        "{:<14} {:<10} {:<18} {:<9}",
        "XDP_REDIRECT", "pps ", "pps-human-readable", "measure-period"
    );
}

#[test]
fn test_stats_print() {
    let now = StatsRecord {
        xdp_redir: [
            Record { counter: 100, timestamp: 200 },
            Record { counter: 40, timestamp: 90 },
        ],
    };
    let prev = StatsRecord {
        xdp_redir: [
            Record { counter: 80, timestamp: 100 },
            Record { counter: 20, timestamp: 30 },
        ],
    };

    // Normal call (header, err_only=0)
    stats_print_headers(false);

    // Simulate stats_print() loop
    for i in 0..REDIR_RES_MAX {
        let r = now.xdp_redir[i];
        let p = prev.xdp_redir[i];
        let period = r.timestamp.wrapping_sub(p.timestamp);
        let packets = r.counter.wrapping_sub(p.counter);
        let mut pps: f64 = 0.0;
        let mut period_: f64 = 0.0;

        if p.timestamp != 0 {
            if period > 0 {
                period_ = (period as f64) / 1_000_000_000.0;
                pps = if period_ > 0.0 { packets as f64 / period_ } else { 0.0 };
            }
        }
        println!(
            "{:<14} {:<10.1} {:<18.1} {}",
            err2str(i as i32).unwrap_or("NULL"),
            pps, pps, period_
        );
    }
    // Error only path
    stats_print_headers(true);
}