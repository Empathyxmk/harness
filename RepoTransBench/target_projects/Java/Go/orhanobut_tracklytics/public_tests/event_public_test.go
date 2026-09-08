package public_tests

import (
	"reflect"
	"testing"
)

type CustomTrackEvent struct{}

func (CustomTrackEvent) Value() string  { return "public_event" }
func (CustomTrackEvent) Filters() []int { return []int{3, 4} }
func (CustomTrackEvent) Tags() []string { return []string{"pub1", "pub2"} }

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

func NewEventFromTrackEvent(te CustomTrackEvent, attrs, superAttrs map[string]interface{}) *Event {
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

func TestConstructorWithDifferentFields(t *testing.T) {
	name := "demo"
	filters := []int{10, 20}
	tags := []string{"alpha", "beta"}
	attrs := map[string]interface{}{"m": "n"}
	superAttrs := map[string]interface{}{"foo": "bar"}
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

func TestConstructorWithDifferentTrackEvent(t *testing.T) {
	te := CustomTrackEvent{}
	attrs := map[string]interface{}{"x": 2}
	superAttrs := map[string]interface{}{"y": "z"}
	ev := NewEventFromTrackEvent(te, attrs, superAttrs)
	if ev.Name != "public_event" {
		t.Fatalf("Expected name public_event, got %s", ev.Name)
	}
	if !reflect.DeepEqual(ev.Filters, []int{3, 4}) {
		t.Fatalf("Expected filters [3 4], got %v", ev.Filters)
	}
	if !reflect.DeepEqual(ev.Tags, []string{"pub1", "pub2"}) {
		t.Fatalf("Expected tags [pub1 pub2], got %v", ev.Tags)
	}
	if !reflect.DeepEqual(ev.Attributes, attrs) {
		t.Fatalf("Expected attributes %v, got %v", attrs, ev.Attributes)
	}
	if !reflect.DeepEqual(ev.SuperAttributes, superAttrs) {
		t.Fatalf("Expected super attributes %v, got %v", superAttrs, ev.SuperAttributes)
	}
}

func TestGetAllAttributesDifferentKeys(t *testing.T) {
	attrs := map[string]interface{}{"jack": "jill"}
	superAttrs := map[string]interface{}{"tango": "fox"}
	ev := NewEvent("n2", []int{}, []string{}, attrs, superAttrs)
	all := ev.GetAllAttributes()
	if len(all) != 2 || all["jack"] != "jill" || all["tango"] != "fox" {
		t.Fatalf("Expected merged attributes, got %v", all)
	}
}

func TestGetAllAttributesSuperOverridesDifferent(t *testing.T) {
	attrs := map[string]interface{}{"theme": "dark", "score": 100}
	superAttrs := map[string]interface{}{"theme": "light"}
	ev := NewEvent("n3", []int{}, []string{}, attrs, superAttrs)
	all := ev.GetAllAttributes()
	if len(all) != 2 || all["theme"] != "light" || all["score"] != 100 {
		t.Fatalf("Expected super attrs override, got %v", all)
	}
}

func TestEmptyAttributesPublic(t *testing.T) {
	ev := NewEvent("public_event", []int{}, []string{}, map[string]interface{}{}, map[string]interface{}{})
	all := ev.GetAllAttributes()
	if len(all) != 0 {
		t.Fatalf("Expected empty map, got %v", all)
	}
}