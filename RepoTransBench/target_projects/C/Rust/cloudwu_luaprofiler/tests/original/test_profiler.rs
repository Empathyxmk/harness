use std::env;
use std::path::PathBuf;
use mlua::prelude::*;
use std::fs;

#[test]
fn test_lua_profiler() {
    // Create Lua state
    let lua = Lua::new();
    
    // Get the current directory to find test.lua
    let current_dir = env::current_dir().expect("Failed to get current directory");
    let test_lua_path = current_dir.join("tests/original/test.lua");
    
    // Make sure test.lua exists
    assert!(test_lua_path.exists(), "test.lua not found at {:?}", test_lua_path);
    
    // Load the test Lua script
    let test_script = fs::read_to_string(test_lua_path)
        .expect("Failed to read test.lua");
    
    // Execute the script
    match lua.load(&test_script).exec() {
        Ok(_) => println!("test_profiler: test run complete"),
        Err(e) => panic!("Lua error: {}", e),
    }
}