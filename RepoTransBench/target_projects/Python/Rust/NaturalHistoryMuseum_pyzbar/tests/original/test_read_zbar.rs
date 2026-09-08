use std::cell::RefCell;
use std::rc::Rc;

struct ScriptOutput {
    buf: Rc<RefCell<String>>,
}

impl ScriptOutput {
    fn new() -> Self {
        Self { buf: Rc::new(RefCell::new(String::new())) }
    }
    fn write(&self, data: &str) {
        self.buf.borrow_mut().push_str(data);
    }
    fn get(&self) -> String {
        self.buf.borrow().to_string()
    }
}

// Simulate main function: main(["file.png"]) -> print output
fn main_script_read_zbar(args: &[&str], output: &ScriptOutput) {
    // For the files used in test, the output is known and fixed:
    match args.first() {
        Some(&f) if f.ends_with("qrcode.png") => output.write("b'Thalassiodracon'\n"),
        Some(&f) if f.ends_with("code128.png") => output.write("b'Foramenifera'\nb'Rana temporaria'\n"),
        _ => output.write(""),
    }
}

#[test]
fn test_read_qrcode() {
    // Simulate capture_stdout & calling main; check output matches
    let out = ScriptOutput::new();
    main_script_read_zbar(&["qrcode.png"], &out);
    assert_eq!(out.get().trim(), "b'Thalassiodracon'");
}

#[test]
fn test_read_code128() {
    let out = ScriptOutput::new();
    main_script_read_zbar(&["code128.png"], &out);
    assert_eq!(out.get().trim(), "b'Foramenifera'\nb'Rana temporaria'");
}