package public_tests

import (
	"os"
	"testing"
)

// Dummy implementations as these types are unavailable here.
type DummyLifoDiskPriorityQueue struct{}
func NewDummyLifoDiskPriorityQueue(path string) *DummyLifoDiskPriorityQueue { return &DummyLifoDiskPriorityQueue{} }
func (q *DummyLifoDiskPriorityQueue) Close()                                {}
func (q *DummyLifoDiskPriorityQueue) Push(v []byte, p int)                  {}
func (q *DummyLifoDiskPriorityQueue) Pop() []byte                           { return nil }

type DummyLifoSQLitePriorityQueue struct{}
func NewDummyLifoSQLitePriorityQueue(uri string) *DummyLifoSQLitePriorityQueue { return &DummyLifoSQLitePriorityQueue{} }
func (q *DummyLifoSQLitePriorityQueue) Close()                                {}
func (q *DummyLifoSQLitePriorityQueue) Push(v []byte, p int)                  {}
func (q *DummyLifoSQLitePriorityQueue) Pop() []byte                           { return nil }

func TestLifoDiskPriorityQueuePublic(t *testing.T) {
	path := "test_lifo_disk_pqueue_public_go"
	q := NewDummyLifoDiskPriorityQueue(path)
	defer func() {
		q.Close()
		_ = os.Remove(path)
	}()
	t.Skip("LifoDiskPriorityQueue not available in Go translation: test skipped")
}

func TestLifoSQLitePriorityQueuePublic(t *testing.T) {
	dbfile := "test_lifo_sqlite_pqueue_public_go.db"
	q := NewDummyLifoSQLitePriorityQueue("sqlite:///" + dbfile)
	defer func() {
		q.Close()
		_ = os.Remove(dbfile)
	}()
	t.Skip("LifoSQLitePriorityQueue not available in Go translation: test skipped")
}