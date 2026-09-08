package original

import (
	"testing"
	"errors"
	"sync"
	"time"

	"github.com/stretchr/testify/assert"
)

// Mock Publisher/Consumer for demonstration
type MessageQueue struct {
	messages []string
	sync.Mutex
}

func NewMessageQueue() *MessageQueue {
	return &MessageQueue{}
}

func (mq *MessageQueue) Publish(msg string) {
	mq.Lock()
	defer mq.Unlock()
	mq.messages = append(mq.messages, msg)
}

func (mq *MessageQueue) Consume() (string, error) {
	mq.Lock()
	defer mq.Unlock()
	if len(mq.messages) == 0 {
		return "", errors.New("empty")
	}
	msg := mq.messages[0]
	mq.messages = mq.messages[1:]
	return msg, nil
}

func TestMessageQueuePublishConsume(t *testing.T) {
	q := NewMessageQueue()
	q.Publish("foo")
	q.Publish("bar")
	msg, err := q.Consume()
	assert.Nil(t, err)
	assert.Equal(t, "foo", msg)
	msg, err = q.Consume()
	assert.Nil(t, err)
	assert.Equal(t, "bar", msg)
	_, err = q.Consume()
	assert.NotNil(t, err)
}

func TestMessageQueueConcurrency(t *testing.T) {
	q := NewMessageQueue()
	var wg sync.WaitGroup

	// Publisher goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := 0; i < 10; i++ {
			q.Publish("msg")
		}
	}()
	time.Sleep(10 * time.Millisecond) // Give time for some messages to appear

	// Consumer goroutine
	consumed := 0
	wg.Add(1)
	go func() {
		defer wg.Done()
		for consumed < 10 {
			_, err := q.Consume()
			if err == nil {
				consumed++
			}
			time.Sleep(1 * time.Millisecond)
		}
	}()
	wg.Wait()
	assert.Equal(t, 10, consumed)
}