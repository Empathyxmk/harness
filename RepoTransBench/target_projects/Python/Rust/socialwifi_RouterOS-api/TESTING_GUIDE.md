# Testing Guide for socialwifi_RouterOS-api

**Project**: socialwifi_RouterOS-api
**Language**: Rust
**Translated from**: Python
**Generated on**: 2025-07-17 12:42:17

## Quick Start

### Run All Tests
```bash
./run_tests.sh
```

### Run Specific Test Categories
```bash
# Run original tests only
./run_tests.sh original

# Run public tests only
./run_tests.sh public

# Run specific test file
./run_tests.sh specific <test_file>

# Clean and rebuild
./run_tests.sh clean

# Show help
./run_tests.sh help
```

## Test Structure

- **Original Tests**: 9 files
- **Public Tests**: 9 files
- **Total Test Files**: 18

### Original Test Files
- `tests/original/test_api_communicator.rs`
- `tests/original/test_base_api.rs`
- `tests/original/test_sentence.rs`
- `tests/original/test_api_structure.rs`
- `tests/original/test_resource.rs`
- `tests/original/test_query.rs`
- `tests/original/test_api_socket.rs`
- `tests/original/test_socket.rs`
- `tests/original/test_login_router_os_api.rs`

### Public Test Files
- `public_tests/test_public_api_communicator.rs`
- `public_tests/test_public_base_api.rs`
- `public_tests/test_public_sentence.rs`
- `public_tests/test_public_api_structure.rs`
- `public_tests/test_public_resource.rs`
- `public_tests/test_public_api_socket.rs`
- `public_tests/test_public_query.rs`
- `public_tests/test_public_login_router_os_api.rs`
- `public_tests/test_public_socket.rs`

## Manual Testing Commands

If you prefer to run tests manually using Rust tools:

### Run All Tests
```bash
cargo test
```

### Run Original Tests
```bash
cargo test --test original
```

### Run Public Tests
```bash
cargo test --test public
```

## Project Structure

```
routeros_api/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── main.rs
├── tests/
│   └── original/
│       ├── test_api_communicator.rs
│       ├── test_base_api.rs
│       ├── test_sentence.rs
│       ├── test_api_structure.rs
│       ├── test_resource.rs
│       ├── test_query.rs
│       ├── test_api_socket.rs
│       ├── test_socket.rs
│       ├── test_login_router_os_api.rs
├── public_tests/
│   ├── test_public_api_communicator.rs
│   ├── test_public_base_api.rs
│   ├── test_public_sentence.rs
│   ├── test_public_api_structure.rs
│   ├── test_public_resource.rs
│   ├── test_public_api_socket.rs
│   ├── test_public_query.rs
│   ├── test_public_login_router_os_api.rs
│   ├── test_public_socket.rs
├── run_tests.sh
├── project_structure.txt
```

## Notes

- This project was automatically translated from the original source code
- Test logic should be identical to the original tests
- If you encounter issues, check the translation_summary.json for details
