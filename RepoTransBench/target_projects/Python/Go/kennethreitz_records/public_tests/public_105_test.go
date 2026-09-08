package public_tests

import (
	"database/sql"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIssue105Public(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE plants (species varchar(32))")
	assert.NoError(t, err)
	_, err = db.Exec("INSERT INTO plants (species) VALUES (?)", "Ficus")
	assert.NoError(t, err)
	rows, err := db.Query("SELECT * FROM plants")
	assert.NoError(t, err)
	defer rows.Close()
	if rows.Next() {
		var species string
		err = rows.Scan(&species)
		assert.NoError(t, err)
		assert.Equal(t, "Ficus", species)
	} else {
		t.Fatal("No data in plants table!")
	}
}