// Translation of: test/unit/test_client_public.c

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

static mut G_TSC_PER_SECOND: u64 = 2_000_000_000; // 2GHz for public

fn rte_rdtsc() -> u64 {
    2_000_000
}

// Mock same as original, but use public test data
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

    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_client_assign_task_less_target_than_cpu_public() {
        let mut cfg = Config { cpu_num: 6, cps: 3, cc: 5, launch_num: 3, wait: 2 };
        let ws0 = WorkSpace { id: 0, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws1 = WorkSpace { id: 1, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws2 = WorkSpace { id: 2, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws3 = WorkSpace { id: 3, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws4 = WorkSpace { id: 4, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws5 = WorkSpace { id: 5, cfg: cfg.clone(), client_launch: ClientLaunch::default() };

        assert_eq!(client_assign_task(&ws0, 3), 1);
        assert_eq!(client_assign_task(&ws1, 3), 1);
        assert_eq!(client_assign_task(&ws2, 3), 1);
        assert_eq!(client_assign_task(&ws3, 3), 0);
        assert_eq!(client_assign_task(&ws4, 3), 0);
        assert_eq!(client_assign_task(&ws5, 3), 0);
    }

    #[test]
    fn test_client_assign_task_more_target_than_cpu_public() {
        let mut cfg = Config { cpu_num: 3, cps: 10, cc: 9, launch_num: 5, wait: 1 };
        let ws0 = WorkSpace { id: 0, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws1 = WorkSpace { id: 1, cfg: cfg.clone(), client_launch: ClientLaunch::default() };
        let ws2 = WorkSpace { id: 2, cfg: cfg.clone(), client_launch: ClientLaunch::default() };

        let ws0_tasks = client_assign_task(&ws0, 10);
        let ws1_tasks = client_assign_task(&ws1, 10);
        let ws2_tasks = client_assign_task(&ws2, 10);
        assert!(ws0_tasks > 0);
        assert!(ws1_tasks > 0);
        assert!(ws2_tasks > 0);
        assert!(ws0_tasks > ws1_tasks);
    }

    #[test]
    fn test_client_init_idle_public() {
        let mut cfg = Config { cpu_num: 2, cps: 0, cc: 0, launch_num: 1, wait: 2 };
        let mut ws = WorkSpace { id: 1, cfg, client_launch: ClientLaunch::default() };
        let ret = client_init(&mut ws);
        assert_eq!(ret, 0);
    }

    #[test]
    fn test_client_init_auto_launch_num_public() {
        let mut cfg = Config { cpu_num: 2, cps: 6, cc: 2, launch_num: 0, wait: 3 };
        let mut ws = WorkSpace { id: 1, cfg, client_launch: ClientLaunch::default() };
        let ret = client_init(&mut ws);
        assert_eq!(ret, 0);
        assert_ne!(ws.cfg.launch_num, 0);
    }

    #[test]
    fn test_client_init_warn_public() {
        let mut cfg = Config { cpu_num: 2, cps: 5, cc: 3, launch_num: 3, wait: 2 };
        let mut ws = WorkSpace { id: 0, cfg, client_launch: ClientLaunch::default() };
        let ret = client_init(&mut ws);
        assert_eq!(ret, 0);
    }
}