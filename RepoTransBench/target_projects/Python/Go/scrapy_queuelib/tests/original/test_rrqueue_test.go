package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// A basic round robin queue with key support.
type RRQueue struct {
	queues map[string][]interface{}
	keys   []string
	idx    int
}

func NewRRQueue() *RRQueue {
	return &RRQueue{
		queues: make(map[string][]interface{}),
	}
}

func (q *RRQueue) Push(val interface{}, key string) {
	if _, ok := q.queues[key]; !ok {
		q.keys = append(q.keys, key)
	}
	q.queues[key] = append(q.queues[key], val)
}

func (q *RRQueue) Pop() interface{} {
	if len(q.keys) == 0 {
		return nil
	}
	startIdx := q.idx
	numKeys := len(q.keys)
	for {
		key := q.keys[q.idx]
		queue := q.queues[key]
		if len(queue) > 0 {
			val := queue[0]
			q.queues[key] = queue[1:]
			// Remove key if its queue is empty
			if len(q.queues[key]) == 0 {
				q.removeKey(q.idx)
			} else {
				q.idx = (q.idx + 1) % len(q.keys)
			}
			return val
		}
		q.removeKey(q.idx)
		if len(q.keys) == 0 || q.idx == startIdx {
			break
		}
	}
	return nil
}

func (q *RRQueue) removeKey(i int) {
	q.keys = append(q.keys[:i], q.keys[i+1:]...)
	if i >= len(q.keys) {
		q.idx = 0
	}
}

func (q *RRQueue) Len() int {
	n := 0
	for _, q2 := range q.queues {
		n += len(q2)
	}
	return n
}

func (q *RRQueue) Close() error {
	return nil
}

func (q *RRQueue) Open() error {
	return nil
}

func (q *RRQueue) Sync() error {
	return nil
}

func TestRRQueue_BasicRoundRobin(t *testing.T) {
	q := NewRRQueue()
	q.Push("a1", "a")
	q.Push("a2", "a")
	q.Push("b1", "b")
	q.Push("a3", "a")
	q.Push("b2", "b")
	q.Push("c1", "c")

	expected := []string{"a1", "b1", "c1", "a2", "b2", "a3"}
	for _, want := range expected {
		got := q.Pop()
		assert.Equal(t, want, got)
	}
	assert.Nil(t, q.Pop())
	assert.Equal(t, 0, q.Len())
}

func TestRRQueue_PushPopOrder(t *testing.T) {
	q := NewRRQueue()
	q.Push("x2", "x")
	q.Push("y1", "y")
	q.Push("z1", "z")
	q.Push("x1", "x")
	q.Push("y2", "y")

	expected := []string{"x2", "y1", "z1", "x1", "y2"}
	for _, want := range expected {
		got := q.Pop()
		assert.Equal(t, want, got)
	}
	assert.Nil(t, q.Pop())
}

func TestRRQueue_CloseOpenSync(t *testing.T) {
	q := NewRRQueue()
	assert.NoError(t, q.Close())
	assert.NoError(t, q.Open())
	assert.NoError(t, q.Sync())
}

func TestRRQueue_Len(t *testing.T) {
	q := NewRRQueue()
	q.Push("a", "k1")
	assert.Equal(t, 1, q.Len())
	q.Push("b", "k1")
	assert.Equal(t, 2, q.Len())
	q.Push("c", "k2")
	assert.Equal(t, 3, q.Len())
	q.Pop()
	assert.Equal(t, 2, q.Len())
	q.Pop()
	q.Pop()
	assert.Equal(t, 0, q.Len())
}

func TestRRQueue_EmptyPop(t *testing.T) {
	q := NewRRQueue()
	assert.Nil(t, q.Pop())
	q.Push("foo", "k")
	assert.Equal(t, "foo", q.Pop())
	assert.Nil(t, q.Pop())
}