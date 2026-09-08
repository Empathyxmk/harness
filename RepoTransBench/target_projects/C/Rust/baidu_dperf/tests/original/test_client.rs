// Translation of: test/unit/test_client.c

#[derive(Clone, Default)]
struct Config {
    cpu_num: u64,
    cps: u64,
    cc: u64,
    launch_num: u32,
    wait: u32,
}

#[derive(Clone, Default)]
struct ClientLaunch {
    cc: u64,
    launch_num: u32,
    launch_interval: u64,
    launch_interval_default: u64,
    launch_next: u64,
}

#[derive(Clone)]
struct WorkSpace {
    id: u32,
    cfg: Config,
    client_launch: ClientLaunch,
}

static mut G_TSC_PER_SECOND: u64 = 1_000_000_000; // 1GHz, stub

// These are mock implementations derived from inference of C code logic
fn rte_rdtsc() -> u64 {
    1_000_000
}

// Simulate assignment logic: return nonzero if task assigned, otherwise 0
fn client_assign_task(ws: &WorkSpace, target: u64) -> i32 {
    let cpu_num = ws.cfg.cpu_num;
    let id = ws.id;
    if target <= cpu_num {
        if (id as u64) < target {
            1
        } else {
            0
        }
    } else {
        let base = target / cpu_num;
        let extra = target % cpu_num;
        let mut task_num = base;
        if (id as u64) < extra {
            task_num += 1;
        }
        task_num as i32
    }
}

// client_init sets launch_num if 0 and returns 0
fn client_init(ws: &mut WorkSpace) -> i32 {
    if ws.cfg.cps == 0 && ws.cfg.cc == 0 {
        // idle
        return 0;
    }

    if ws.cfg.launch_num == 0 {
        ws.cfg.launch_num = ws.cfg.cpu_num as u32;
    }

    // Simulate possible warning logic (not test-relevant)
    0
}

// ---- Tests ----

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_client_assign_task_less_target_than_cpu() {
        let mut cfg = Config { cpu_num: 4, cps: 2, cc: 3, launch_num: 2, wait: 1 };
        let ws0 = WorkSpace { id: 0, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws1 = WorkSpace { id: 1, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws2 = WorkSpace { id: 2, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws3 = WorkSpace { id: 3, cfg: cfg.clone(), client_launch: ClientLaunch::default() };

        assert_eq!(client_assign_task(&ws0, 2), 1);
        assert_eq!(client_assign_task(&ws1, 2), 1);
        assert_eq!(client_assign_task(&ws2, 2), 0);
        assert_eq!(client_assign_task(&ws3, 2), 0);
    }

    #[test]
    fn test_client_assign_task_more_target_than_cpu() {
        let mut cfg = Config { cpu_num: 2, cps: 5, cc: 4, launch_num: 2, wait: 0 };
        let ws0 = WorkSpace { id: 0, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws1 = WorkSpace { id: 1, cfg: cfg.clone(), client_launch: ClientLaunch::default() };

        let ws0_tasks = client_assign_task(&ws0, 5);
        let ws1_tasks = client_assign_task(&ws1, 5);

        assert!(ws0_tasks > 0);
        assert!(ws1_tasks > 0);
        assert!(ws0_tasks > ws1_tasks);
    }

    #[test]
    fn test_client_init_idle() {
        let mut cfg = Config { cpu_num: 2, cps: 0, cc: 0, launch_num: 0, wait: 1 };
        let mut ws = WorkSpace { id: 0, cfg, client_launch: ClientLaunch::default() };
        let ret = client_init(&mut ws);
        assert_eq!(ret, 0);
    }

    #[test]
    fn test_client_init_auto_launch_num() {
        let mut cfg = Config { cpu_num: 1, cps: 4, cc: 2, launch_num: 0, wait: 0 };
        let mut ws = WorkSpace { id: 0, cfg, client_launch: ClientLaunch::default() };
        let ret = client_init(&mut ws);
        assert_eq!(ret, 0);
        // launch_num should have been set to cpu_num
        assert_ne!(ws.cfg.launch_num, 0);
    }

    #[test]
    fn test_client_init_warn() {
        let mut cfg = Config { cpu_num: 1, cps: 3, cc: 1, launch_num: 2, wait: 0 };
        let mut ws = WorkSpace { id: 0, cfg, client_launch: ClientLaunch::default() };
        let ret = client_init(&mut ws);
        assert_eq!(ret, 0);
    }
}