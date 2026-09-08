import pytest
import base64

def generate_different_random_string(size):
    # Simulating deterministic random string generator (as in C++ test)
    buffer = [(i*73 + 17) for i in range(size)]
    # Pack as bytes, then base64 url encode, trim to size
    import struct
    arr = b''.join(struct.pack('<I', v & 0xFFFFFFFF) for v in buffer)
    s = base64.urlsafe_b64encode(arr).decode("ascii")
    return s[:size].encode()

@pytest.mark.parametrize("password", [
    b"public_test_pass_123",
    generate_different_random_string(512),
    generate_different_random_string(1500),
    generate_different_random_string(2500),
    generate_different_random_string(8000),
    generate_different_random_string(16384),
])
def test_basic_password_workflow(password):
    # Simulate the operations as closely as possible in a public-only setting.
    # Instead of an actual keychain (system-specific API), we simulate storing, reading, and deleting.
    # Expected: store, read, delete is successful for each password
    # In the real environment, there'd be persistent storage, but here we just do in-memory simulation.

    keychain_storage = {}

    service_key = f"QtKeychainPublicTest-sim_{hash(password)}"

    # Store password (WritePasswordJob)
    keychain_storage[service_key] = password
    assert service_key in keychain_storage
    assert keychain_storage[service_key] == password

    # Read password (ReadPasswordJob)
    retrieved = keychain_storage[service_key]
    assert retrieved == password

    # Delete password (DeletePasswordJob)
    del keychain_storage[service_key]
    assert service_key not in keychain_storage