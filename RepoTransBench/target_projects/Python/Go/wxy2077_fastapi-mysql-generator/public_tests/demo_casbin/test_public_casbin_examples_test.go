package demo_casbin

import (
	"testing"
	"os"
	"path/filepath"

	"github.com/casbin/casbin/v2"
	"github.com/stretchr/testify/assert"
)

func publicDirPath(t *testing.T) string {
	dir, err := os.Getwd()
	if err != nil {
		t.Fatalf("failed to determine working dir")
	}
	return dir
}

func Test01DemoEnforcementPublic(t *testing.T) {
	dirPath := publicDirPath(t)
	modelPath := filepath.Join(dirPath, "model.conf")
	policyPath := filepath.Join(dirPath, "policy.csv")
	e, err := casbin.NewEnforcer(modelPath, policyPath)
	if err != nil {
		t.Fatalf("Failed creating enforcer: %v", err)
	}
	assert.False(t, e.Enforce("alice2", "data2", "write"))
	assert.True(t, e.Enforce("alice2", "data2", "read"))
	assert.False(t, e.Enforce("bob2", "data2", "read"))
	assert.True(t, e.Enforce("bob2", "data2", "write"))
	assert.False(t, e.Enforce("bob2", "data1", "read"))
	assert.True(t, e.Enforce("root2", "data1", "delete"))
	assert.False(t, e.Enforce("root2", "data1", "update"))
}

func Test02OrmAdapterPublic(t *testing.T) {
	dirPath := publicDirPath(t)
	modelPath := filepath.Join(dirPath, "model.conf")
	policyPath := filepath.Join(dirPath, "policy.csv")
	e, err := casbin.NewEnforcer(modelPath, policyPath)
	if err != nil {
		t.Fatalf("Failed creating enforcer: %v", err)
	}
	assert.True(t, e.Enforce("alice2", "data2", "read"))
	assert.False(t, e.Enforce("alice2", "data2", "write"))
}

func Test03CustomOrmPublic(t *testing.T) {
	dirPath := publicDirPath(t)
	modelPath := filepath.Join(dirPath, "custom_model.conf")
	policyFile := filepath.Join(os.TempDir(), "custom_policy.csv")
	content := "p, john, domain_public, data9, access\np, jane, domain_public, data9, read\np, john, domain_public, data10, modify\n"
	err := os.WriteFile(policyFile, []byte(content), 0644)
	if err != nil {
		t.Fatalf("failed writing policy file: %v", err)
	}
	defer os.Remove(policyFile)
	e, err := casbin.NewEnforcer(modelPath, policyFile)
	if err != nil {
		t.Fatalf("Failed creating enforcer: %v", err)
	}
	assert.True(t, e.Enforce("john", "domain_public", "data9", "access"))
	assert.False(t, e.Enforce("john", "domain_public", "data9", "read"))
	assert.True(t, e.Enforce("john", "domain_public", "data10", "modify"))
	assert.False(t, e.Enforce("jane", "domain_public", "data9", "access"))
	assert.True(t, e.Enforce("jane", "domain_public", "data9", "read"))
}