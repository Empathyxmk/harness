mod cemu {
    pub mod os {
        #[derive(Clone, Debug, PartialEq, Eq)]
        pub struct OperatingSystem(pub String);
        impl OperatingSystem {
            pub fn new(s: &str) -> Self { OperatingSystem(s.to_ascii_lowercase()) }
        }

        pub static Linux: OperatingSystem = OperatingSystem("linux".to_string());
        pub static Windows: OperatingSystem = OperatingSystem("windows".to_string());

        impl std::fmt::Display for OperatingSystem {
            fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                write!(f, "{}", match self.0.as_str() {
                    "linux" => "Linux",
                    "windows" => "Windows",
                    s => s
                })
            }
        }
        pub trait Fspath {
            fn __fspath__(&self) -> &str;
        }
        impl Fspath for OperatingSystem {
            fn __fspath__(&self) -> &str {
                self.0.as_str()
            }
        }
        impl PartialEq<str> for OperatingSystem {
            fn eq(&self, other: &str) -> bool {
                self.0.eq_ignore_ascii_case(other)
            }
        }
        impl PartialEq<OperatingSystem> for OperatingSystem {
            fn eq(&self, other: &OperatingSystem) -> bool {
                self.0 == other.0
            }
        }
    }
}

#[test]
fn test_operating_system_str_fspath_eq() {
    use cemu::os::{Linux, Windows, OperatingSystem, Fspath};
    // __str__ and __fspath__
    assert_eq!(format!("{}", Linux), "Linux");
    assert_eq!(Linux.__fspath__(), "linux");
    // __eq__ with str
    assert!(Linux == "linux");
    assert!(Linux == "LiNUX");
    // __eq__ with object
    assert!(Linux == cemu::os::OperatingSystem("linux".to_string()));
    assert!(Windows != Linux);
    // __eq__ wrong type (simulate with an Option/wrapper error)
    let result = std::panic::catch_unwind(|| {
        let _ = Linux == 42; // Should produce compile-error; simulate type check error.
    });
    assert!(result.is_err());
}

#[test]
fn test_operating_system_eq_case() {
    use cemu::os::OperatingSystem;
    let a = OperatingSystem::new("AnOS");
    let b = OperatingSystem::new("AnOS");
    let c = OperatingSystem::new("anotherOS");
    assert!(a == b);
    assert!(!(a == c));
}