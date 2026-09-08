// Rust translation of tests/test_xml_attacks.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsel::Selector;
    use sysinfo::{System, SystemExt, ProcessExt};

    static MIB_1: u64 = 1024 * 1024;

    // Helper to load local test XML (simulate file loading)
    fn load_attack(name: &str) -> String {
        // In a real test, load from a testdata directory.
        // Here, return the known "billion_laughs" string.
        // For demonstration, use a trivial xml.
        if name == "billion_laughs" {
            return r#"
                <?xml version="1.0"?>
                <!DOCTYPE lolz [
                <!ENTITY lol "lol">
                <!ENTITY lol1 "&lol;&lol;">
                <!ENTITY lol2 "&lol1;&lol1;">
                <!ENTITY lol3 "&lol2;&lol2;">
                <!ENTITY lol4 "&lol3;&lol3;">
                <!ENTITY lol5 "&lol4;&lol4;">
                <!ENTITY lol6 "&lol5;&lol5;">
                <!ENTITY lol7 "&lol6;&lol6;">
                <!ENTITY lol8 "&lol7;&lol7;">
                <!ENTITY lol9 "&lol8;&lol8;">
                ]>
                <lolz>&lol9;</lolz>
            "#.to_string();
        }
        "".to_string()
    }

    #[test]
    fn test_billion_laughs() {
        let mut sys = System::new();
        sys.refresh_processes();
        let before = sys.process(sysinfo::get_current_pid().unwrap()).unwrap().memory();
        let selector = Selector::from_xml(load_attack("billion_laughs").as_str());
        let lolz = selector.css("lolz::text").get().unwrap();
        sys.refresh_processes();
        let after = sys.process(sysinfo::get_current_pid().unwrap()).unwrap().memory();
        let diff = after as i64 - before as i64;
        assert!(diff <= MIB_1 as i64, "Memory change: {}B", diff);
        assert_eq!(lolz, "&lol9;");
    }
}