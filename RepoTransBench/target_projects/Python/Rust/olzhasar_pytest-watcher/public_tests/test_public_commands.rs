use crate::commands::{Manager, Command};

use crate::config::Config;
use crate::terminal::Terminal;
use crate::trigger::Trigger;

struct AnotherDummyCommand {
    pub was_run: bool,
}
impl Default for AnotherDummyCommand {
    fn default() -> Self { Self { was_run: false } }
}
impl Command for AnotherDummyCommand {
    fn character() -> &'static str { "9" }
    fn caption() -> &'static str { "nine" }
    fn description() -> &'static str { "another test" }
    fn show_in_menu() -> bool { true }
    fn run(
        &mut self,
        _trigger: &mut crate::trigger::Trigger,
        _term: &mut crate::terminal::Terminal,
        _config: &mut crate::config::Config,
    ) {
        self.was_run = true;
    }
}

#[test]
fn test_run_alternate_command() {
    let mut trig = Trigger::new();
    let mut config = Config::new();
    let mut term = Terminal::new();
    let mut cmd = AnotherDummyCommand::default();
    assert_eq!(cmd.was_run, false);
    cmd.run(&mut trig, &mut term, &mut config);
    assert_eq!(cmd.was_run, true);
}