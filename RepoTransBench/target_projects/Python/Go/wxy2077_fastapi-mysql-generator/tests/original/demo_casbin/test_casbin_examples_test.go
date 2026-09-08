package demo_casbin

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/casbin/casbin/v2"
	sqladapter "github.com/casbin/sqlalchemy-adapter/v2"
	"github.com/stretchr/testify/assert"
)

func getDirPath(t *testing.T) string {
	dir, err := os.Getwd()
	if err != nil {
		t.Fatalf("failed to determine working dir")
	}
	return dir
}

func Test01DemoEnforcement(t *testing.T) {
	dirPath := getDirPath(t)
	modelPath := filepath.Join(dirPath, "model.conf")
	policyPath := filepath.Join(dirPath, "policy.csv")
	e, err := casbin.NewEnforcer(modelPath, policyPath)
	if err != nil {
		t.Fatalf("Failed creating enforcer: %v", err)
	}

	assert.True(t, e.Enforce("nick", "data1", "read"))
	assert.False(t, e.Enforce("nick", "data1", "write"))
	// Add a new policy and test
	ok, _ := e.AddPolicy("alice", "data2", "read")
	assert.True(t, ok)
	assert.True(t, e.Enforce("alice", "data2", "read"))
	// Remove and test
	ok, _ = e.RemovePolicy("alice", "data2", "read")
	assert.True(t, ok)
	assert.False(t, e.Enforce("alice", "data2", "read"))
}

func Test02OrmAdapter(t *testing.T) {
	dirPath := getDirPath(t)
	tmpDB := "test_orm.db"
	dbURL := "sqlite:///" + filepath.Join(os.TempDir(), tmpDB)
	adapter, err := sqladapter.NewAdapter(dbURL)
	if err != nil {
		t.Fatalf("failed to create adapter: %v", err)
	}
	modelPath := filepath.Join(dirPath, "model.conf")
	e, err := casbin.NewEnforcer(modelPath, adapter)
	if err != nil {
		t.Fatalf("NewEnforcer error: %v", err)
	}
	ok, _ := e.AddPolicy("bob", "resource1", "read")
	assert.True(t, ok)
	assert.True(t, e.Enforce("bob", "resource1", "read"))
	ok, _ = e.RemovePolicy("bob", "resource1", "read")
	assert.True(t, ok)
	assert.False(t, e.Enforce("bob", "resource1", "read"))
}

func paramsMatchGo(fullNameK1, key2 string) bool {
	key1 := fullNameK1
	if idx := len(fullNameK1); idx > 0 {
		questionIdx := -1
		for i := 0; i < len(fullNameK1); i++ {
			if fullNameK1[i] == '?' {
				questionIdx = i
				break
			}
		}
		if questionIdx != -1 {
			key1 = fullNameK1[:questionIdx]
		}
	}
	// KeyMatch2: path pattern matching - mimic python's casbin.util.key_match2
	// In Go: casbin's built-in Fn is available to enforcer, so we skip full logic.
	return casbin.KeyMatch2(key1, key2)
}

func Test03CustomOrmParamMatch(t *testing.T) {
	dirPath := getDirPath(t)
	adapter, err := sqladapter.NewAdapter("sqlite:///memory.db")
	if err != nil {
		t.Fatalf("adapter error: %v", err)
	}
	modelPath := filepath.Join(dirPath, "custom_model.conf")
	e, err := casbin.NewEnforcer(modelPath, adapter)
	if err != nil {
		t.Fatalf("NewEnforcer error: %v", err)
	}
	_ = e.AddFunction("ParamsMatch", func(args ...interface{}) (interface{}, error) {
		if len(args) < 2 {
			return false, nil
		}
		k1, ok1 := args[0].(string)
		k2, ok2 := args[1].(string)
		if !ok1 || !ok2 {
			return false, nil
		}
		return paramsMatchGo(k1, k2), nil
	})
	// Add policy for GET on /api/user
	ok, _ := e.AddPolicy("999", "/api/user", "GET")
	assert.True(t, ok)
	// Should permit GET on /api/user?aaa=1
	assert.True(t, e.Enforce("999", "/api/user?aaa=1", "GET"))
	// Should deny GET on /api/admin?aaa=1
	assert.False(t, e.Enforce("999", "/api/admin?aaa=1", "GET"))
	ok, _ = e.RemovePolicy("999", "/api/user", "GET")
	assert.True(t, ok)
	assert.False(t, e.Enforce("999", "/api/user?aaa=1", "GET"))
}