package public_tests

import (
	"os"
	"strings"
	"testing"
)

func TestPublicFakeVaultFile(t *testing.T) {
	f, err := os.CreateTemp("", "public_vaultfile")
	if err != nil {
		t.Fatalf("could not create fake public vault file: %v", err)
	}
	defer os.Remove(f.Name())
	content := "$ANSIBLE_VAULT;1.1;AES256\ntestpublic"
	_, err = f.WriteString(content)
	if err != nil {
		t.Fatalf("could not write content: %v", err)
	}
	f.Close()
	data, err := os.ReadFile(f.Name())
	if err != nil {
		t.Fatalf("could not read back vault file: %v", err)
	}
	if !strings.Contains(string(data), "$ANSIBLE_VAULT") {
		t.Error("vault file missing magic string")
	}
	if !strings.Contains(string(data), "public") {
		t.Error("vault file missing public string")
	}
}

func TestPublicVaultPassword(t *testing.T) {
	f, err := os.CreateTemp("", "public_vaultpass")
	if err != nil {
		t.Fatalf("could not create vault password file: %v", err)
	}
	defer os.Remove(f.Name())
	pass := "superpublicpw"
	_, err = f.WriteString(pass)
	if err != nil {
		t.Fatalf("could not write password: %v", err)
	}
	f.Close()
	readBytes, err := os.ReadFile(f.Name())
	if err != nil {
		t.Fatalf("could not read password file: %v", err)
	}
	if string(readBytes) != pass {
		t.Errorf("password mismatch: got %q want %q", string(readBytes), pass)
	}
}

func TestPublicMultipleVaultFiles(t *testing.T) {
	contents := []string{
		"$ANSIBLE_VAULT;1.2;AES256\npublicvaultcipher",
		"$ANSIBLE_VAULT;1.2;AES256\nanotherpubliccipher",
	}
	for i, c := range contents {
		f, err := os.CreateTemp("", "vault_varied.public")
		if err != nil {
			t.Fatalf("failed to temp vault file %v: %v", i, err)
		}
		defer os.Remove(f.Name())
		_, err = f.WriteString(c)
		if err != nil {
			t.Fatalf("could not write vault content %d: %v", i, err)
		}
		f.Close()
		readBytes, err := os.ReadFile(f.Name())
		if err != nil {
			t.Fatalf("could not read: %v", err)
		}
		if !strings.Contains(string(readBytes), "AES256") {
			t.Errorf("vault file missing AES256: %q", string(readBytes))
		}
	}
}