use crate::watcher;

#[test]
fn test_imports_and_main_loop_present() {
    // Make sure that main_loop exists (function pointer is some fn)
    let _f: fn(&mut crate::trigger::Trigger, &mut crate::config::Config, &mut crate::terminal::Terminal) = crate::watcher::main_loop;
}