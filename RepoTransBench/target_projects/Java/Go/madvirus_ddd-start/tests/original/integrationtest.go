package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyDB struct {
	data map[string]string
}

func (db *DummyDB) Put(key, value string) {
	if db.data == nil {
		db.data = map[string]string{}
	}
	db.data[key] = value
}

func (db *DummyDB) Get(key string) string {
	return db.data[key]
}

func IntegrationService(db *DummyDB, input string) string {
	db.Put("result", input+"_saved")
	return db.Get("result")
}

func TestIntegrationService(t *testing.T) {
	db := &DummyDB{}
	result := IntegrationService(db, "abc")
	assert.Equal(t, "abc_saved", result)
}