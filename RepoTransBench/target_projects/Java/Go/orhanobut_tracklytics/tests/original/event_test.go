package original

import (
	"reflect"
	"testing"
)

type DummyTrackEvent struct{}

func (DummyTrackEvent) Value() string  { return "dummy_event" }
func (DummyTrackEvent) Filters() []int { return []int{1, 2} }
func (DummyTrackEvent) Tags() []string { return []string{"tag1", "tag2"} }

type Event struct {
	Name           string
	Filters        []int
	Tags           []string
	Attributes     map[string]interface{}
	SuperAttributes map[string]interface{}
}

func NewEvent(name string, filters []int, tags []string, attrs, superAttrs map[string]interface{}) *Event {
	return &Event{
		Name:           name,
		Filters:        filters,
		Tags:           tags,
		Attributes:     attrs,
		SuperAttributes: superAttrs,
	}
}

func NewEventFromTrackEvent(te DummyTrackEvent, attrs, superAttrs map[string]interface{}) *Event {
	return &Event{
		Name:           te.Value(),
		Filters:        te.Filters(),
		Tags:           te.Tags(),
		Attributes:     attrs,
		SuperAttributes: superAttrs,
	}
}

func (e *Event) GetAllAttributes() map[string]interface{} {
	result := make(map[string]interface{})
	for k, v := range e.Attributes {
		result[k] = v
	}
	for k, v := range e.SuperAttributes {
		result[k] = v
	}
	return result
}

func TestConstructorWithFields(t *testing.T) {
	name := "test"
	filters := []int{1, 2}
	tags := []string{"t1", "t2"}
	attrs := map[string]interface{}{"a": "b"}
	superAttrs := map[string]interface{}{"x": "y"}
	ev := NewEvent(name, filters, tags, attrs, superAttrs)
	if ev.Name != name {
		t.Fatalf("Expected name %s, got %s", name, ev.Name)
	}
	if !reflect.DeepEqual(ev.Filters, filters) {
		t.Fatalf("Expected filters %v, got %v", filters, ev.Filters)
	}
	if !reflect.DeepEqual(ev.Tags, tags) {
		t.Fatalf("Expected tags %v, got %v", tags, ev.Tags)
	}
	if !reflect.DeepEqual(ev.Attributes, attrs) {
		t.Fatalf("Expected attributes %v, got %v", attrs, ev.Attributes)
	}
	if !reflect.DeepEqual(ev.SuperAttributes, superAttrs) {
		t.Fatalf("Expected super attributes %v, got %v", superAttrs, ev.SuperAttributes)
	}
}

func TestConstructorWithTrackEvent(t *testing.T) {
	te := DummyTrackEvent{}
	attrs := map[string]interface{}{"c": 1}
	superAttrs := map[string]interface{}{}
	ev := NewEventFromTrackEvent(te, attrs, superAttrs)
	if ev.Name != "dummy_event" {
		t.Fatalf("Expected name dummy_event, got %s", ev.Name)
	}
	if !reflect.DeepEqual(ev.Filters, []int{1, 2}) {
		t.Fatalf("Expected filters [1 2], got %v", ev.Filters)
	}
	if !reflect.DeepEqual(ev.Tags, []string{"tag1", "tag2"}) {
		t.Fatalf("Expected tags [tag1 tag2], got %v", ev.Tags)
	}
	if !reflect.DeepEqual(ev.Attributes, attrs) {
		t.Fatalf("Expected attributes %v, got %v", attrs, ev.Attributes)
	}
	if !reflect.DeepEqual(ev.SuperAttributes, superAttrs) {
		t.Fatalf("Expected super attributes %v, got %v", superAttrs, ev.SuperAttributes)
	}
}

func TestGetAllAttributesNoOverlap(t *testing.T) {
	attrs := map[string]interface{}{"foo": "bar"}
	superAttrs := map[string]interface{}{"hello": "world"}
	ev := NewEvent("n", []int{}, []string{}, attrs, superAttrs)
	all := ev.GetAllAttributes()
	if len(all) != 2 || all["foo"] != "bar" || all["hello"] != "world" {
		t.Fatalf("Expected merged attributes, got %v", all)
	}
}

func TestGetAllAttributesSuperOverridesNormal(t *testing.T) {
	attrs := map[string]interface{}{"foo": "bar", "a": 1}
	superAttrs := map[string]interface{}{"foo": "baz"}
	ev := NewEvent("n", []int{}, []string{}, attrs, superAttrs)
	all := ev.GetAllAttributes()
	if len(all) != 2 || all["foo"] != "baz" || all["a"] != 1 {
		t.Fatalf("Expected super attrs override, got %v", all)
	}
}

func TestEmptyAttributes(t *testing.T) {
	ev := NewEvent("event", []int{}, []string{}, map[string]interface{}{}, map[string]interface{}{})
	all := ev.GetAllAttributes()
	if len(all) != 0 {
		t.Fatalf("Expected empty map, got %v", all)
	}
}