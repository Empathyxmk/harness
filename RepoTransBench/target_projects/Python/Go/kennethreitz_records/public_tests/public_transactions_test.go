package public_tests

import (
	"database/sql"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestTransactionsCommitPublic(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE books (isbn varchar(13), title text)")
	assert.NoError(t, err)
	tx, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO books (isbn, title) VALUES (?, ?)", "1234567890123", "Great Book")
	assert.NoError(t, err)
	assert.NoError(t, tx.Commit())
	row := db.QueryRow("SELECT * FROM books WHERE isbn = ?", "1234567890123")
	var isbn string
	var title string
	err = row.Scan(&isbn, &title)
	assert.NoError(t, err)
	assert.Equal(t, "Great Book", title)
}

func TestTransactionsRollbackPublic(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE t1 (foo text)")
	assert.NoError(t, err)
	tx, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO t1 (foo) VALUES (?)", "tempvalue")
	assert.NoError(t, err)
	err = tx.Rollback()
	assert.NoError(t, err)
	rows, err := db.Query("SELECT * FROM t1")
	assert.NoError(t, err)
	defer rows.Close()
	assert.False(t, rows.Next())
}

func TestTransactionsNestedPublic(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE t2 (id integer)")
	assert.NoError(t, err)
	tx1, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx1.Exec("INSERT INTO t2 (id) VALUES (?)", 1)
	assert.NoError(t, err)
	tx2, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx2.Exec("INSERT INTO t2 (id) VALUES (?)", 2)
	assert.NoError(t, err)
	assert.NoError(t, tx2.Commit())
	assert.NoError(t, tx1.Commit())
	rows, err := db.Query("SELECT * FROM t2")
	assert.NoError(t, err)
	defer rows.Close()
	ids := map[int]struct{}{}
	for rows.Next() {
		var id int
		assert.NoError(t, rows.Scan(&id))
		ids[id] = struct{}{}
	}
	assert.Equal(t, map[int]struct{}{1: {}, 2: {}}, ids)
}

func TestTransactionsMultiStatementCommitPublic(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE accounts (id integer, balance integer)")
	assert.NoError(t, err)
	tx, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO accounts (id, balance) VALUES (?, ?)", 1, 200)
	assert.NoError(t, err)
	_, err = tx.Exec("UPDATE accounts SET balance = balance + 150")
	assert.NoError(t, err)
	assert.NoError(t, tx.Commit())
	row := db.QueryRow("SELECT balance FROM accounts WHERE id = 1")
	var balance int
	assert.NoError(t, row.Scan(&balance))
	assert.Equal(t, 350, balance)
}

func TestTransactionsContextManagerReturnPublic(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE chess (piece text)")
	assert.NoError(t, err)
	tx, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO chess (piece) VALUES (?)", "rook")
	assert.NoError(t, err)
	assert.NoError(t, tx.Commit())
	row := db.QueryRow("SELECT piece FROM chess")
	var piece string
	assert.NoError(t, row.Scan(&piece))
	assert.Equal(t, "rook", piece)
}

func TestTransactionsRollbackExceptionInstancePublic(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	assert.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("CREATE TABLE mus (sound text)")
	assert.NoError(t, err)
	tx, err := db.Begin()
	assert.NoError(t, err)
	_, err = tx.Exec("INSERT INTO mus (sound) VALUES (?)", "chirp")
	assert.NoError(t, err)
	assert.NoError(t, tx.Rollback())
	rows, err := db.Query("SELECT * FROM mus")
	assert.NoError(t, err)
	defer rows.Close()
	assert.False(t, rows.Next())
}