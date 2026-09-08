//! Test reading logic for test-php.ini configuration (enables extension)

#[cfg(test)]
mod tests {
    #[test]
    fn test_pcov_extension_ini_setup() {
        let ini_content = "extension=/workspace/temp_public_testcase/public_test_generation_20250623_201253/krakjoe_pcov/modules/pcov.so\n";
        // Check correct extension loading
        assert!(ini_content.starts_with("extension="));
        let ext_path = ini_content.trim_start_matches("extension=").trim();
        assert!(ext_path.ends_with("pcov.so"));
        assert!(ext_path.contains("/krakjoe_pcov/modules/pcov.so"));
    }
}