# Testing Guide for ramonhagenaars_jsons

**Project**: ramonhagenaars_jsons
**Language**: Rust
**Translated from**: Python
**Generated on**: 2025-07-17 10:25:53

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

- **Original Tests**: 16 files
- **Public Tests**: 0 files
- **Total Test Files**: 16

### Original Test Files
- `tests/original/test_common_impl.rs`
- `tests/original/test_compatibility_impl.rs`
- `tests/original/test_counter.rs`
- `tests/original/test_defaultdict.rs`
- `tests/original/test_dict_hashkey.rs`
- `tests/original/test_fork.rs`
- `tests/original/test_list.rs`
- `tests/original/test_ordered_dict.rs`
- `tests/original/test_performance.rs`
- `tests/original/test_primitive.rs`
- `tests/original/test_set.rs`
- `tests/original/test_sconstruct.rs`
- `tests/original/test_specific_versions.rs`
- `tests/original/test_time.rs`
- `tests/original/test_type_error.rs`
- `tests/original/test_version.rs`

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
ramonhagenaars_jsons/
├── Cargo.toml
├── LICENSE
├── README.md
├── SConstruct.py
├── docs/
│   ├── _templates/
│   │   └── sidebarintro.html
│   ├── api.rst
│   ├── conf.py
│   ├── faq.rst
│   └── index.rst
├── htmlcov/
│   └── ... (coverage output files)
├── jsons/
│   └── ... (library python files)
├── tests/
│   └── original/
│       ├── test_common_impl.rs
│       ├── test_compatibility_impl.rs
│       ├── test_counter.rs
│       ├── test_defaultdict.rs
│       ├── test_dict_hashkey.rs
│       ├── test_fork.rs
│       ├── test_list.rs
│       ├── test_ordered_dict.rs
│       ├── test_performance.rs
│       ├── test_primitive.rs
│       ├── test_set.rs
│       ├── test_sconstruct.rs
│       ├── test_specific_versions.rs
│       ├── test_time.rs
│       ├── test_type_error.rs
│       ├── test_version.rs
```

## Notes

- This project was automatically translated from the original source code
- Test logic should be identical to the original tests
- If you encounter issues, check the translation_summary.json for details
