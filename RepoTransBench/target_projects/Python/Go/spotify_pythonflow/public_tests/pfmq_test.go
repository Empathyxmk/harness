package public_tests

import (
	"testing"
	"errors"

	"github.com/stretchr/testify/assert"
)

// Simple message queue for public tests
type TestQueue struct {
	data []string
}

func (q *TestQueue) Publish(s string) {
	q.data = append(q.data, s)
}
func (q *TestQueue) Pop() (string, error) {
	if len(q.data) == 0 {
		return "", errors.New("empty queue")
	}
	x := q.data[0]
	q.data = q.data[1:]
	return x, nil
}

func TestTestQueuePublic(t *testing.T) {
	q := &TestQueue{}
	q.Publish("abc")
	v, err := q.Pop()
	assert.Nil(t, err)
	assert.Equal(t, "abc", v)
	_, err = q.Pop()
	assert.NotNil(t, err)
}