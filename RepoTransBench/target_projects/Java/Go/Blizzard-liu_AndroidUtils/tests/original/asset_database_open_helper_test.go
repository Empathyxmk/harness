package original

import (
    "errors"
    "testing"
)

type mockContext struct {
    dbName string
}

func (m *mockContext) GetDatabaseName() string {
    return m.dbName
}

type assetDBHelper struct {
    ctx    *mockContext
    dbName string
    // simulate error trigger
    triggerIOError bool
}

func (a *assetDBHelper) GetDatabaseName() string {
    return a.dbName
}
func (a *assetDBHelper) GetWritableDatabase() error {
    if a.triggerIOError {
        return errors.New("fail")
    }
    return nil
}

func TestGetDatabaseName(t *testing.T) {
    ctx := &mockContext{dbName: "mydb.db"}
    helper := &assetDBHelper{ctx: ctx, dbName: "mydb.db"}
    if helper.GetDatabaseName() != "mydb.db" {
        t.Errorf("Expected dbName mydb.db, got %v", helper.GetDatabaseName())
    }
}

func TestGetWritableDatabaseIOException(t *testing.T) {
    helper := &assetDBHelper{triggerIOError: true}
    err := helper.GetWritableDatabase()
    if err == nil {
        t.Fatalf("Expected error from GetWritableDatabase(), got nil")
    }
}