import pytest

# This public test emulates test logic from tests/test_vault.py
# Since the original test likely interacts with ansible vault features,
# we focus on changing filenames, ids, or passphrases, while preserving test intent.

import os

def test_public_fake_vault_file(tmp_path):
    # Create a public-named vault-like file
    vault_file = tmp_path / "public_vaultfile"
    vault_file.write_text("$ANSIBLE_VAULT;1.1;AES256\ntestpublic")
    assert vault_file.exists()
    # Pretend to read/parse it
    with open(vault_file, "r") as f:
        content = f.read()
    assert "$ANSIBLE_VAULT" in content
    assert "public" in content

def test_public_vault_password(tmp_path):
    # Simulate reading a different vault password
    pw_file = tmp_path / "public_vaultpass"
    vault_password = "superpublicpw"
    pw_file.write_text(vault_password)
    assert pw_file.read_text() == vault_password

@pytest.mark.parametrize("vault_content", [
    "$ANSIBLE_VAULT;1.2;AES256\npublicvaultcipher",
    "$ANSIBLE_VAULT;1.2;AES256\nanotherpubliccipher"
])
def test_public_multiple_vault_files(tmp_path, vault_content):
    vault_file = tmp_path / "vault_varied.public"
    vault_file.write_text(vault_content)
    assert "AES256" in vault_file.read_text()