use crate::commands::{Manager, DummyCommand};
use crate::config::Config;
use crate::terminal::Terminal;
use crate::trigger::Trigger;

#[test]
fn test_run_command() {
    // Setup DummyCommand in the registry (simulation)
    let mut trigger = Trigger::new();
    let mut config = Config::new();
    let mut mock_terminal = Terminal::new();
    let mut dummy = DummyCommand { invoked: false };
    let character = DummyCommand::character();
    // Simulating registry by direct usage.
    assert!(!dummy.invoked);
    dummy.run(&mut trigger, &mut mock_terminal, &mut config);
    assert!(dummy.invoked);
}