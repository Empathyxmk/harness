#!/bin/bash
set -e

echo '[*] Running original tests...'
cargo test --test registry_persistence --test domain_info --test portscan -- --nocapture

echo '[*] Running public tests...'
cargo test --test registry_persistence_public --test domain_info_public --test portscan_public -- --nocapture

echo '[*] All tests completed successfully!'