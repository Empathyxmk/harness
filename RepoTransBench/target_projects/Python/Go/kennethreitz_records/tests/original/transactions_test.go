package original

import (
	"database/sql"
	"testing"

	"github.com/stretchr/testify/assert"
	"kennethreitz_records/tests"
)

func TestPlainDB(t *testing.T) {
	db, cleanup := tests.GetTestDB(t)
	defer cleanup()
	drop := tests.SetupFooTable(t, db)
	defer drop()

	_, err := db.Exec("INSERT INTO foo VALUES (42);")
	assert.NoError(t, err)
	_, err = db.Exec("INSERT INTO foo VALUES (43);")
	assert.NoError(t, err)

	var count int
	err = db.QueryRow("SELECT count(*) as n FROM foo;").Scan(&count)
	assert.NoError(t, err)
	assert.Equal(t, 2, count)
}

func TestPlainConn(t *testing.T) {
	db, cleanup := tests.GetTestDB(t)
	defer cleanup()
	drop := tests.SetupFooTable(t, db)
	defer drop()

	conn, err := db.Conn(nil)
	assert.NoError(t, err)
	defer conn.Close()

	_, err = conn.ExecContext(nil, "INSERT INTO foo VALUES (42);")
	assert.NoError(t, err)
	_, err = conn.ExecContext(nil, "INSERT INTO foo VALUES (43);")
	assert.NoError(t, err)

	var count int
	row := conn.QueryRowContext(nil, "SELECT count(*) as n FROM foo;")
	err = row.Scan(&count)
	assert.NoError(t, err)
	assert.Equal(t, 2, count)
}

func TestFailingTransactionSelfManaged(t *testing.T) {
	db, cleanup := tests.GetTestDB(t)
	defer cleanup()
	drop := tests.SetupFooTable(t, db)
	defer drop()

	conn, err := db.Conn(nil)
	assert.NoError(t, err)
	defer conn.Close()

	tx, err := conn.BeginTx(nil, nil)
	assert.NoError(t, err)
	defer func() {
		tx.Rollback()
	}()
	_, err = tx.ExecContext(nil, "INSERT INTO foo VALUES (42);")
	assert.NoError(t, err)
	_, err = tx.ExecContext(nil, "INSERT INTO foo VALUES (43);")
	assert.NoError(t, err)

	// Simulate failure and rollback
	_ = tx.Rollback()

	var count int
	row := db.QueryRow("SELECT count(*) as n FROM foo;")
	err = row.Scan(&count)
	assert.NoError(t, err)
	assert.Equal(t, 0, count)
}

func TestFailingTransaction(t *testing.T) {
	db, cleanup := tests.GetTestDB(t)
	defer cleanup()
	drop := tests.SetupFooTable(t, db)
	defer drop()

	tx, err := db.Begin()
	assert.NoError(t, err)

	_, err = tx.Exec("INSERT INTO foo VALUES (42);")
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO foo VALUES (43);")
	assert.NoError(t, err)

	_ = tx.Rollback() // Failure triggered -> rollback

	var count int
	err = db.QueryRow("SELECT count(*) as n FROM foo;").Scan(&count)
	assert.NoError(t, err)
	assert.Equal(t, 0, count)
}

func TestPassingTransactionSelfManaged(t *testing.T) {
	db, cleanup := tests.GetTestDB(t)
	defer cleanup()
	drop := tests.SetupFooTable(t, db)
	defer drop()

	conn, err := db.Conn(nil)
	assert.NoError(t, err)
	defer conn.Close()

	tx, err := conn.BeginTx(nil, nil)
	assert.NoError(t, err)
	_, err = tx.ExecContext(nil, "INSERT INTO foo VALUES (42);")
	assert.NoError(t, err)
	_, err = tx.ExecContext(nil, "INSERT INTO foo VALUES (43);")
	assert.NoError(t, err)

	err = tx.Commit()
	assert.NoError(t, err)
	// Conn close handled in defer above

	var count int
	err = db.QueryRow("SELECT count(*) as n FROM foo;").Scan(&count)
	assert.NoError(t, err)
	assert.Equal(t, 2, count)
}

func TestPassingTransaction(t *testing.T) {
	db, cleanup := tests.GetTestDB(t)
	defer cleanup()
	drop := tests.SetupFooTable(t, db)
	defer drop()

	tx, err := db.Begin()
	assert.NoError(t, err)

	_, err = tx.Exec("INSERT INTO foo VALUES (42);")
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO foo VALUES (43);")
	assert.NoError(t, err)

	err = tx.Commit()
	assert.NoError(t, err)

	var count int
	err = db.QueryRow("SELECT count(*) as n FROM foo;").Scan(&count)
	assert.NoError(t, err)
	assert.Equal(t, 2, count)
}