use crate::watcher;

#[test]
fn test_public_import_all_watcher_module_names() {
    // Check some attribute on watcher
    let _main_loop: fn(&mut crate::trigger::Trigger, &mut crate::config::Config, &mut crate::terminal::Terminal) = watcher::main_loop;
}