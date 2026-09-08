package public_tests

import (
	"database/sql"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIssue69Public(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()

	_, err = db.Exec("CREATE table animals (species text)")
	assert.NoError(t, err)
	_, err = db.Exec("SELECT * FROM animals WHERE species = ?", "CanisLupus")
	assert.NoError(t, err)
}