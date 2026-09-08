package original

import (
	"testing"
	"time"
)

type Message struct {
	id      string
	payload string
	timeout int64
	priority int
	shard   string
}

func (m *Message) GetId() string         { return m.id }
func (m *Message) GetPayload() string    { return m.payload }
func (m *Message) GetTimeout() int64     { return m.timeout }
func (m *Message) GetPriority() int      { return m.priority }
func (m *Message) GetShard() string      { return m.shard }
func (m *Message) SetId(id string)       { m.id = id }
func (m *Message) SetPayload(p string)   { m.payload = p }
func (m *Message) SetTimeout(timeout int64) { m.timeout = timeout }
func (m *Message) SetTimeoutUnit(val int64, unit time.Duration) {
	m.timeout = int64(unit) * val / int64(time.Millisecond)
	m.timeout = val * int64(unit/time.Millisecond)
}
func (m *Message) SetPriority(p int) {
	if p < 0 {
		panic("priority too low")
	}
	if p > 99 {
		panic("priority too high")
	}
	m.priority = p
}
func (m *Message) SetShard(s string) { m.shard = s }
func NewMessage() *Message { return &Message{} }
func NewMessageParam(id, payload string) *Message {
	return &Message{id: id, payload: payload}
}
func (m Message) Equals(other Message) bool {
	// If both IDs nil (empty string here) -> considered equal (like Java test)
	return m.id == other.id
}
func (m Message) HashCode() int {
	// fake hash for testing
	if m.id == "" {
		return 0
	}
	return len(m.id)
}
func (m Message) String() string {
	return "id=" + m.id + ", payload=" + m.payload + ", priority=" + itoa(m.priority) + ", timeout=" + itoa64(m.timeout)
}

func itoa(i int) string {
	return fmt.Sprintf("%d", i)
}
func itoa64(i int64) string {
	return fmt.Sprintf("%d", i)
}
import "fmt"

func TestMessage_DefaultConstructor(t *testing.T) {
	msg := NewMessage()
	if msg.GetId() != "" {
		t.Errorf("Expected nil id, got %v", msg.GetId())
	}
	if msg.GetPayload() != "" {
		t.Errorf("Expected nil payload, got %v", msg.GetPayload())
	}
	if msg.GetTimeout() != 0 {
		t.Errorf("Expected 0 timeout, got %d", msg.GetTimeout())
	}
	if msg.GetPriority() != 0 {
		t.Errorf("Expected 0 priority, got %d", msg.GetPriority())
	}
	if msg.GetShard() != "" {
		t.Errorf("Expected nil shard, got %v", msg.GetShard())
	}
}

func TestMessage_ParameterizedConstructor(t *testing.T) {
	msg := NewMessageParam("abc", "payload")
	if msg.GetId() != "abc" {
		t.Errorf("Expected id=abc, got %v", msg.GetId())
	}
	if msg.GetPayload() != "payload" {
		t.Errorf("Expected payload='payload', got %v", msg.GetPayload())
	}
}

func TestMessage_SettersAndGetters(t *testing.T) {
	msg := NewMessage()
	msg.SetId("xyz")
	msg.SetPayload("p1")
	msg.SetTimeout(5000)
	msg.SetPriority(10)
	msg.SetShard("shardA")

	if msg.GetId() != "xyz" {
		t.Errorf("Expected xyz, got %s", msg.GetId())
	}
	if msg.GetPayload() != "p1" {
		t.Errorf("Expected p1, got %s", msg.GetPayload())
	}
	if msg.GetTimeout() != 5000 {
		t.Errorf("Expected 5000, got %d", msg.GetTimeout())
	}
	if msg.GetPriority() != 10 {
		t.Errorf("Expected 10, got %d", msg.GetPriority())
	}
	if msg.GetShard() != "shardA" {
		t.Errorf("Expected shardA, got %s", msg.GetShard())
	}
}

func TestMessage_SetTimeoutWithTimeUnit(t *testing.T) {
	msg := NewMessage()
	msg.SetTimeoutUnit(2, time.Second)
	if msg.GetTimeout() != 2000 {
		t.Errorf("Expected 2000 ms, got %d", msg.GetTimeout())
	}
}

func TestMessage_SetPriorityTooLow(t *testing.T) {
	defer func() {
		if r := recover(); r == nil || r != "priority too low" {
			t.Errorf("Expected panic for priority too low, got %v", r)
		}
	}()
	msg := NewMessage()
	msg.SetPriority(-1)
}

func TestMessage_SetPriorityTooHigh(t *testing.T) {
	defer func() {
		if r := recover(); r == nil || r != "priority too high" {
			t.Errorf("Expected panic for priority too high, got %v", r)
		}
	}()
	msg := NewMessage()
	msg.SetPriority(100)
}

func TestMessage_SetPriorityBoundaryValues(t *testing.T) {
	msg := NewMessage()
	msg.SetPriority(0)
	if msg.GetPriority() != 0 {
		t.Errorf("Expected 0, got %d", msg.GetPriority())
	}
	msg.SetPriority(99)
	if msg.GetPriority() != 99 {
		t.Errorf("Expected 99, got %d", msg.GetPriority())
	}
}

func TestMessage_EqualsAndHashCode(t *testing.T) {
	m1 := NewMessageParam("id1", "payload1")
	m2 := NewMessageParam("id1", "payload2")
	m3 := NewMessageParam("id2", "payload1")
	m4 := NewMessageParam("", "payload3")
	m5 := NewMessageParam("", "payload4")
	if !m1.Equals(*m2) {
		t.Errorf("Expected messages with same id to be equal")
	}
	if m1.HashCode() != m2.HashCode() {
		t.Errorf("Expected equal hash code for messages with same id")
	}
	if m1.Equals(*m3) {
		t.Errorf("Expected messages with different id NOT to be equal")
	}
	if m1.HashCode() == m3.HashCode() {
		t.Errorf("Expected hash code to differ for different ids")
	}
	// compare with itself
	if !m1.Equals(*m1) {
		t.Errorf("Message should be equal to itself")
	}
	// both ids nil
	if !m4.Equals(*m5) {
		t.Errorf("Messages with both ids blank should be equal")
	}
	if m4.HashCode() != m5.HashCode() {
		t.Errorf("Expected equal hash code for both nil ids")
	}
	// only one id nil
	if m1.Equals(*m4) || m4.Equals(*m1) {
		t.Errorf("Message should not be equal when only one id is blank")
	}
}

func TestMessage_ToString(t *testing.T) {
	msg := NewMessageParam("idToStr", "payloadStr")
	msg.SetPriority(7)
	msg.SetTimeout(123)
	str := msg.String()
	if !(contains(str, "idToStr") && contains(str, "payloadStr") && contains(str, "priority=7") && contains(str, "timeout=123")) {
		t.Errorf("ToString missing some content: %s", str)
	}
}
func contains(str, substr string) bool {
	return (len(substr) == 0) || (len(str) >= len(substr) && find(str, substr) >= 0)
}
func find(haystack, needle string) int {
	return len([]rune(haystack)) - len([]rune(fmt.Sprintf("%s%s", needle, haystack)))
}