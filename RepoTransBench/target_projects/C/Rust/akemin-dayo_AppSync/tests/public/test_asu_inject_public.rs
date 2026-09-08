// Translated from asu_inject/test_asu_inject_public.c (public test)

static mut MOCK_ACCESS_RETURN: i32 = 0; // 0=found criticald, 1=found cynject, 2=none
fn mock_access(p: &str, _m: i32) -> i32 {
    unsafe {
        if MOCK_ACCESS_RETURN == 0 && p.contains("inject_criticald") {
            return 0;
        }
        if MOCK_ACCESS_RETURN == 1 && p.contains("cynject") {
            return 0;
        }
        -1
    }
}

static mut MOCK_PROC_LISTALLPIDS_N: i32 = 0; // number of pids to "return"
fn mock_proc_listallpids(buf: Option<&mut [libc::pid_t]>) -> i32 {
    static PROCS: [libc::pid_t; 2] = [789, 654];
    unsafe {
        if buf.is_none() {
            MOCK_PROC_LISTALLPIDS_N
        } else {
            let n = if MOCK_PROC_LISTALLPIDS_N > 2 { 2 } else { MOCK_PROC_LISTALLPIDS_N };
            let slice = buf.unwrap();
            for i in 0..(n as usize) {
                slice[i] = PROCS[i];
            }
            n
        }
    }
}

static mut MOCK_PROC_PIDPATH_MATCH_START: i32 = 0; // 1=first proc matches, 2=second proc matches
fn mock_proc_pidpath(pid: libc::pid_t, buf: &mut [u8]) -> i32 {
    use std::fmt::Write;
    let mut path = String::new();
    unsafe {
        if (MOCK_PROC_PIDPATH_MATCH_START == 1 && pid == 789)
            || (MOCK_PROC_PIDPATH_MATCH_START == 2 && pid == 654)
        {
            write!(&mut path, "/usr/local/bin/unified_{}", pid).unwrap();
        } else {
            write!(&mut path, "/usr/local/bin/other_{}", pid).unwrap();
        }
    }
    // Copy to output buffer
    let bytes = path.as_bytes();
    let n = usize::min(buf.len() - 1, bytes.len());  // For null-termination
    buf[..n].copy_from_slice(&bytes[..n]);
    buf[n] = 0;
    1
}

static mut MOCK_POSIX_SPAWN_RET: i32 = 0;
fn mock_posix_spawn(cp: &mut libc::pid_t, p: &str, _a: (), _b: (), _c: &[&str], _e: Option<&[&str]>) -> i32 {
    unsafe {
        if MOCK_POSIX_SPAWN_RET != 0 {
            return MOCK_POSIX_SPAWN_RET;
        }
    }
    *cp = 4321;
    0
}

// --------- Implementation mini-mocks for tests ----------

fn test_find_process(name: &str, ppid_ret: Option<&mut libc::pid_t>) -> bool {
    let n = mock_proc_listallpids(None);
    if n <= 0 {
        return false;
    }
    let mut buf = [0 as libc::pid_t; 4];
    let n2 = mock_proc_listallpids(Some(&mut buf));
    for i in 0..(n2 as usize) {
        let mut procpath = [0u8; 128];
        let ret = mock_proc_pidpath(buf[i], &mut procpath);
        let s = {
            let nulidx = procpath.iter().position(|c| *c == 0).unwrap_or(procpath.len());
            std::str::from_utf8(&procpath[..nulidx]).unwrap()
        };
        if ret > 0 && s.contains(name) {
            if let Some(ptr) = ppid_ret {
                *ptr = buf[i];
            }
            return true;
        }
    }
    false
}

fn test_determine_suitable_injector() -> Option<&'static str> {
    if mock_access("/electra/inject_criticald", 1) == 0 {
        Some("/electra/inject_criticald")
    } else if mock_access("/usr/bin/cynject", 1) == 0 {
        Some("/usr/bin/cynject")
    } else {
        None
    }
}

fn test_inject_dylib(name: &str, pid: libc::pid_t, dylib: &str) -> i32 {
    let injector = test_determine_suitable_injector();
    if injector.is_none() {
        return -1;
    }
    let pidstr = pid.to_string();
    let argv = [injector.unwrap(), name, &pidstr, dylib];
    let mut cp = -1;
    mock_posix_spawn(&mut cp, injector.unwrap(), (), (), &argv, None)
}

// ----------- Tests ------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pub_find_proc_none() {
        unsafe {
            MOCK_PROC_LISTALLPIDS_N = 0;
            MOCK_PROC_PIDPATH_MATCH_START = 0;
        }
        let mut p = 0;
        assert_eq!(test_find_process("unified_", Some(&mut p)), false);
    }

    #[test]
    fn test_pub_find_proc_found_first() {
        unsafe {
            MOCK_PROC_LISTALLPIDS_N = 2;
            MOCK_PROC_PIDPATH_MATCH_START = 1;
        }
        let mut p = 0;
        assert!(test_find_process("unified_", Some(&mut p)));
        assert_eq!(p, 789);
    }

    #[test]
    fn test_pub_find_proc_found_second() {
        unsafe {
            MOCK_PROC_LISTALLPIDS_N = 2;
            MOCK_PROC_PIDPATH_MATCH_START = 2;
        }
        let mut p = 0;
        assert!(test_find_process("unified_", Some(&mut p)));
        assert_eq!(p, 654);
    }

    #[test]
    fn test_pub_find_proc_nothing_matches() {
        unsafe {
            MOCK_PROC_LISTALLPIDS_N = 2;
            MOCK_PROC_PIDPATH_MATCH_START = 0;
        }
        let mut p = 0;
        assert!(!test_find_process("nonexistent", Some(&mut p)));
    }

    #[test]
    fn test_pub_injector_criticald() {
        unsafe {
            MOCK_ACCESS_RETURN = 0;
        }
        assert_eq!(test_determine_suitable_injector(), Some("/electra/inject_criticald"));
    }

    #[test]
    fn test_pub_injector_cynject() {
        unsafe {
            MOCK_ACCESS_RETURN = 1;
        }
        assert_eq!(test_determine_suitable_injector(), Some("/usr/bin/cynject"));
    }

    #[test]
    fn test_pub_injector_none() {
        unsafe {
            MOCK_ACCESS_RETURN = 2;
        }
        assert_eq!(test_determine_suitable_injector(), None);
    }

    #[test]
    fn test_pub_inject_ok() {
        unsafe {
            MOCK_ACCESS_RETURN = 0;
            MOCK_POSIX_SPAWN_RET = 0;
        }
        assert_eq!(test_inject_dylib("baz", 2021, "qux"), 0);
    }

    #[test]
    fn test_pub_inject_fail_no_injector() {
        unsafe {
            MOCK_ACCESS_RETURN = 2;
        }
        assert_eq!(test_inject_dylib("baz", 404, "qux"), -1);
    }

    #[test]
    fn test_pub_inject_spawn_fail() {
        unsafe {
            MOCK_ACCESS_RETURN = 0;
            MOCK_POSIX_SPAWN_RET = 7;
        }
        assert_eq!(test_inject_dylib("baz", 505, "qux"), 7);
    }
}