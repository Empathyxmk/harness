// Dummy stub for the error module
mod cemu {
    pub mod errors {
        #[derive(Debug)]
        pub struct AssemblyException(String);
        impl AssemblyException {
            pub fn new(msg: &str) -> Self {
                AssemblyException(msg.to_owned())
            }
        }
        impl std::fmt::Display for AssemblyException {
            fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                write!(f, "{}", self.0)
            }
        }
        impl std::error::Error for AssemblyException {}
    }
}

#[test]
fn test_assembly_exception() {
    use cemu::errors::AssemblyException;
    let e = AssemblyException::new("msg");
    assert!(e.to_string() == "msg");
}