package public_tests

import (
	"testing"
	"time"
	"fmt"
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
	return m.id == other.id
}
func (m Message) HashCode() int {
	if m.id == "" {
		return 0
	}
	return len(m.id)
}
func (m Message) String() string {
	return "id=" + m.id + ", payload=" + m.payload + ", priority=" + itoa(m.priority) + ", timeout=" + itoa64(m.timeout)
}
func itoa(i int) string      { return fmt.Sprintf("%d", i) }
func itoa64(i int64) string { return fmt.Sprintf("%d", i) }
func contains(str, substr string) bool { return (len(substr) == 0) || (len(str) >= len(substr) && find(str, substr) >= 0) }
func find(haystack, needle string) int { return len([]rune(haystack)) - len([]rune(fmt.Sprintf("%s%s", needle, haystack))) }

func TestMessagePublic_DefaultConstructor(t *testing.T) {
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

func TestMessagePublic_ParameterizedConstructor(t *testing.T) {
	msg := NewMessageParam("def", "data")
	if msg.GetId() != "def" {
		t.Errorf("Expected id=def, got %v", msg.GetId())
	}
	if msg.GetPayload() != "data" {
		t.Errorf("Expected payload='data', got %v", msg.GetPayload())
	}
}

func TestMessagePublic_SettersAndGetters(t *testing.T) {
	msg := NewMessage()
	msg.SetId("uvw")
	msg.SetPayload("payloadX")
	msg.SetTimeout(12000)
	msg.SetPriority(5)
	msg.SetShard("shardB")

	if msg.GetId() != "uvw" {
		t.Errorf("Expected uvw, got %s", msg.GetId())
	}
	if msg.GetPayload() != "payloadX" {
		t.Errorf("Expected payloadX, got %s", msg.GetPayload())
	}
	if msg.GetTimeout() != 12000 {
		t.Errorf("Expected 12000, got %d", msg.GetTimeout())
	}
	if msg.GetPriority() != 5 {
		t.Errorf("Expected 5, got %d", msg.GetPriority())
	}
	if msg.GetShard() != "shardB" {
		t.Errorf("Expected shardB, got %s", msg.GetShard())
	}
}

func TestMessagePublic_SetTimeoutWithTimeUnit(t *testing.T) {
	msg := NewMessage()
	msg.SetTimeoutUnit(3, time.Minute)
	if msg.GetTimeout() != 180000 {
		t.Errorf("Expected 180000 ms, got %d", msg.GetTimeout())
	}
}

func TestMessagePublic_SetPriorityTooLow(t *testing.T) {
	defer func() {
		if r := recover(); r == nil || r != "priority too low" {
			t.Errorf("Expected panic for priority too low, got %v", r)
		}
	}()
	msg := NewMessage()
	msg.SetPriority(-5)
}

func TestMessagePublic_SetPriorityTooHigh(t *testing.T) {
	defer func() {
		if r := recover(); r == nil || r != "priority too high" {
			t.Errorf("Expected panic for priority too high, got %v", r)
		}
	}()
	msg := NewMessage()
	msg.SetPriority(150)
}

func TestMessagePublic_SetPriorityBoundaryValues(t *testing.T) {
	msg := NewMessage()
	msg.SetPriority(1)
	if msg.GetPriority() != 1 {
		t.Errorf("Expected 1, got %d", msg.GetPriority())
	}
	msg.SetPriority(98)
	if msg.GetPriority() != 98 {
		t.Errorf("Expected 98, got %d", msg.GetPriority())
	}
}

func TestMessagePublic_EqualsAndHashCode(t *testing.T) {
	m1 := NewMessageParam("idX", "payload3")
	m2 := NewMessageParam("idX", "payload4")
	m3 := NewMessageParam("idY", "payload3")
	m4 := NewMessageParam("", "payloadA")
	m5 := NewMessageParam("", "payloadB")
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
	if !m1.Equals(*m1) {
		t.Errorf("Message should be equal to itself")
	}
	if !m4.Equals(*m5) {
		t.Errorf("Messages with both ids blank should be equal")
	}
	if m4.HashCode() != m5.HashCode() {
		t.Errorf("Expected equal hash code for both nil ids")
	}
	if m1.Equals(*m4) || m4.Equals(*m1) {
		t.Errorf("Message should not be equal when only one id is blank")
	}
}

func TestMessagePublic_ToString(t *testing.T) {
	msg := NewMessageParam("idToString", "payloadTest")
	msg.SetPriority(12)
	msg.SetTimeout(999)
	str := msg.String()
	if !(contains(str, "idToString") && contains(str, "payloadTest") && contains(str, "priority=12") && contains(str, "timeout=999")) {
		t.Errorf("ToString missing some content: %s", str)
	}
}