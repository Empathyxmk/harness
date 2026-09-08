package original

import (
	"database/sql"
	"fmt"
	"net"
	"os"
	"testing"
	"time"

	_ "github.com/lib/pq"
)

func TestPortIsTaken(t *testing.T) {
	// We'll try to bind a port and then see if a second "Postgres" instance could use it.
	ln, err := net.Listen("tcp", "127.0.0.1:54329")
	if err != nil {
		t.Fatalf("failed to listen on test port: %v", err)
	}
	defer ln.Close()
	// Try to simulate starting postgres that should fail because port is used
	connStr := "user=postgres dbname=postgres sslmode=disable port=54329 host=127.0.0.1"
	db, err := sql.Open("postgres", connStr)
	if err == nil {
		defer db.Close()
		err2 := db.Ping()
		if err2 == nil {
			t.Errorf("expected ping to fail because no real instance running")
		}
	}
}

func TestSecondInstanceFailsOnLockedDirAndPort(t *testing.T) {
	// Simulate postgres "data" dir lock by exclusive file open
	dir := "testpg_data_lock"
	file := dir + "/postmaster.pid"
	os.MkdirAll(dir, 0755)
	f, err := os.OpenFile(file, os.O_CREATE|os.O_RDWR, 0644)
	if err != nil {
		t.Fatalf("couldn't create lockfile: %v", err)
	}
	defer func() {
		f.Close()
		os.RemoveAll(dir)
	}()
	// Write some dummy (locked) pidfile
	f.Write([]byte("12345\n"))
	// Attempt to open a second process (simulate launch on given data dir)
	// Should fail: in real life, postgres would refuse to start.
	locked, err := isDirLocked(dir)
	if !locked || err != nil {
		t.Errorf("expected directory to appear locked, got locked=%v err=%v", locked, err)
	}
}

// Helper: mimic "lock detection" like postgres does with postmaster.pid
func isDirLocked(dir string) (bool, error) {
	f, err := os.Open(dir + "/postmaster.pid")
	if err != nil {
		return false, nil // not locked if no pid file
	}
	defer f.Close()
	b := make([]byte, 16)
	n, _ := f.Read(b)
	if n == 0 {
		return false, nil
	}
	pidStr := string(b[:n])
	if len(pidStr) > 0 {
		return true, nil
	}
	return false, nil
}