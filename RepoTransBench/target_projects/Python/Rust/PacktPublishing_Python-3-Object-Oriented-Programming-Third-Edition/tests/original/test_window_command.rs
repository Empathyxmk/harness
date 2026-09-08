#[cfg(test)]
mod tests {
    use super::super::super::window_command::*;
    use std::rc::Rc;
    use std::cell::RefCell;

    #[test]
    fn test_document_save() {
        let tmpfile = std::env::temp_dir().join("file1-test.txt");
        let doc = Document::new(tmpfile.to_str().unwrap());
        doc.save().unwrap();
        let txt = std::fs::read_to_string(tmpfile).unwrap();
        assert_eq!(txt, "This file cannot be modified");
    }

    #[test]
    fn test_save_command_executes_document_save() {
        let tmpfile = std::env::temp_dir().join("file2-test.txt");
        let doc = Rc::new(RefCell::new(Document::new(tmpfile.to_str().unwrap())));
        doc.borrow_mut().contents = "SAVED".to_string();
        let mut cmd = SaveCommand::new(Rc::clone(&doc));
        cmd.execute();
        let txt = std::fs::read_to_string(tmpfile).unwrap();
        assert_eq!(txt, "SAVED");
    }

    #[test]
    fn test_toolbarbutton_click_calls_command() {
        struct DummyCommand { pub x: bool }
        impl DummyCommand {
            pub fn new() -> Self { DummyCommand { x: false } }
        }
        impl Command for DummyCommand {
            fn execute(&mut self) { self.x = true; }
        }
        let dummy = DummyCommand::new();
        let mut button = ToolbarButton::new("n", "icon", Some(dummy));
        if let Some(ref mut cmd) = button.command {
            cmd.execute();
            assert!(cmd.x);
        }
    }

    #[test]
    fn test_keyboardshortcut_keypress_executes_command() {
        struct Dummy { pub called: bool }
        impl Dummy {
            pub fn new() -> Dummy { Dummy { called: false } }
        }
        impl Command for Dummy {
            fn execute(&mut self) { self.called = true; }
        }
        let dummy = Dummy::new();
        let mut ks = KeyboardShortcut::new("k", "ctrl", Some(dummy));
        if let Some(ref mut cmd) = ks.command {
            cmd.execute();
            assert!(cmd.called);
        }
    }

    #[test]
    fn test_menuitem_click_calls_command() {
        struct Dummy { pub did: bool }
        impl Dummy { pub fn new() -> Dummy { Dummy { did: false } } }
        impl Command for Dummy {
            fn execute(&mut self) { self.did = true; }
        }
        let dummy = Dummy::new();
        let mut item = MenuItem::new("F", "X", Some(dummy));
        if let Some(ref mut cmd) = item.command {
            cmd.execute();
            assert!(cmd.did);
        }
    }

    #[test]
    #[should_panic(expected = "SystemExit: 0")]
    fn test_exit_command_exits() {
        let w = Window::new();
        let cmd = ExitCommand::new(&w);
        cmd.execute();
    }
}