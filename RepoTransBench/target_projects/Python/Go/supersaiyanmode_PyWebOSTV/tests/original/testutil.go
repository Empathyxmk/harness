package original

import (
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"sync"
	"time"
)

// Message represents a message sent/received from TV.
type Message map[string]interface{}

type Queue struct {
	mu     sync.Mutex
	items  []interface{}
	closed bool
	cond   *sync.Cond
}

func NewQueue() *Queue {
	q := &Queue{}
	q.cond = sync.NewCond(&q.mu)
	return q
}

func (q *Queue) Put(item interface{}) {
	q.mu.Lock()
	defer q.mu.Unlock()
	if q.closed {
		return
	}
	q.items = append(q.items, item)
	q.cond.Signal()
}

func (q *Queue) Get(block bool, timeoutSecs float64) (interface{}, error) {
	q.mu.Lock()
	defer q.mu.Unlock()
	var timer <-chan time.Time
	if block && timeoutSecs > 0 {
		timer = time.After(time.Duration(timeoutSecs*float64(time.Second)))
	}
	for len(q.items) == 0 && !q.closed {
		if !block {
			return nil, errors.New("queue empty")
		}
		if timer != nil {
			qc := make(chan struct{})
			go func() {
				q.cond.Wait()
				close(qc)
			}()
			select {
			case <-qc:
			case <-timer:
				return nil, errors.New("timeout")
			}
		} else {
			q.cond.Wait()
		}
	}
	if len(q.items) == 0 {
		return nil, errors.New("queue closed")
	}
	item := q.items[0]
	q.items = q.items[1:]
	return item, nil
}

func (q *Queue) Close() {
	q.mu.Lock()
	q.closed = true
	q.cond.Broadcast()
	q.mu.Unlock()
}

type FakeClient struct {
	SentMessages  []Message                // Collect all sent messages for assertion
	sentMu        sync.Mutex
	SentMessage   Message
	Subscriptions map[string]func(Message)
	SubRespQueues map[string][]Message
	RespMu        sync.Mutex
	respCbs       map[string][]func(Message)
	// Used for callbacks passed in send_message
	cbByReqID     map[string]func(Message)
}

func NewFakeClient() *FakeClient {
	return &FakeClient{
		SentMessages:  make([]Message, 0),
		Subscriptions: make(map[string]func(Message)),
		SubRespQueues: make(map[string][]Message),
		respCbs:       make(map[string][]func(Message)),
		cbByReqID:     make(map[string]func(Message)),
	}
}

func (c *FakeClient) SendMessage(msgtype, uri string, payload map[string]interface{}, uniqueID string, callback func(Message), getQueue bool) *Queue {
	msg := make(Message)
	msg["type"] = msgtype
	msg["uri"] = uri
	if uniqueID != "" {
		msg["id"] = uniqueID
	}
	if payload != nil {
		msg["payload"] = payload
	}
	c.sentMu.Lock()
	c.SentMessage = msg
	c.SentMessages = append(c.SentMessages, msg)
	c.sentMu.Unlock()
	if callback != nil && uniqueID != "" {
		c.cbByReqID[uniqueID] = callback
	}
	if getQueue {
		return NewQueue()
	}
	return nil
}

func (c *FakeClient) assertSentMessage(expected map[string]interface{}) bool {
	c.sentMu.Lock()
	defer c.sentMu.Unlock()
	out, _ := json.Marshal(c.SentMessage)
	exp, _ := json.Marshal(expected)
	return string(out) == string(exp)
}

func (c *FakeClient) AssertSentMessage(t TestingT, expected map[string]interface{}) {
	if !c.assertSentMessage(expected) {
		t.Errorf("Sent message does not match. Got: %+v ; expected: %+v", c.SentMessage, expected)
	}
}

func (c *FakeClient) AssertSentMessageWithoutID(t TestingT, expected map[string]interface{}) {
	// Remove id field before comparing if needed
	c.sentMu.Lock()
	defer c.sentMu.Unlock()
	msgCopy := make(map[string]interface{})
	for k, v := range c.SentMessage {
		if k == "id" {
			continue
		}
		msgCopy[k] = v
	}
	out, _ := json.Marshal(msgCopy)
	exp, _ := json.Marshal(expected)
	if string(out) != string(exp) {
		t.Errorf("Sent message does not match (ignoring id). Got: %+v ; expected: %+v", msgCopy, expected)
	}
}

func (c *FakeClient) SetupResponse(uri string, response map[string]interface{}) {
	// For simulating "setup_response", just store for lookup
	if c.SubRespQueues == nil {
		c.SubRespQueues = make(map[string][]Message)
	}
	msg := make(Message)
	for k, v := range response {
		msg[k] = v
	}
	c.SubRespQueues[uri] = []Message{msg}
}

func (c *FakeClient) SetupSubscribeResponse(uri string, responses []map[string]interface{}) {
	if c.SubRespQueues == nil {
		c.SubRespQueues = make(map[string][]Message)
	}
	messages := []Message{}
	for _, resp := range responses {
		msg := make(Message)
		for k, v := range resp {
			msg[k] = v
		}
		messages = append(messages, msg)
	}
	c.SubRespQueues[uri] = messages
}

func (c *FakeClient) ReceivedMessage(msgStr string) {
	// used in subscription tests
	var msg Message
	if err := json.Unmarshal([]byte(msgStr), &msg); err != nil {
		return
	}
	id, _ := msg["id"].(string)
	if cb, ok := c.cbByReqID[id]; ok {
		cb(msg)
	}
}

func (c *FakeClient) Subscribe(uri, id string, callback func(Message)) {
	c.Subscriptions[id] = callback
}

func (c *FakeClient) Unsubscribe(id string) error {
	if _, ok := c.Subscriptions[id]; !ok {
		return errors.New("not found")
	}
	delete(c.Subscriptions, id)
	return nil
}

// TestingT is just a subset of *testing.T for passing into helpers.
type TestingT interface {
	Errorf(format string, args ...interface{})
}

type FakeMouseClient struct {
	Messages []string
	mu       sync.Mutex
}

func NewFakeMouseClient() *FakeMouseClient {
	return &FakeMouseClient{Messages: make([]string, 0)}
}

func (c *FakeMouseClient) AssertSentMessage(t TestingT, expected string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	found := false
	for _, m := range c.Messages {
		if m == expected {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Expected mouse message: %q. Messages: %+v", expected, c.Messages)
	}
}

func (c *FakeMouseClient) Send(msg string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.Messages = append(c.Messages, msg)
}

// For application simulation
type Application struct {
	Data map[string]interface{}
}

func NewApplication(data map[string]interface{}) *Application {
	return &Application{
		Data: data,
	}
}