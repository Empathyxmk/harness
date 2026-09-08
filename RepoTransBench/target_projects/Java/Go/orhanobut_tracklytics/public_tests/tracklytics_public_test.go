package public_tests

import (
	"testing"
)

type Event struct {
	Name           string
	Filters        []int
	Tags           []string
	Attributes     map[string]interface{}
	SuperAttributes map[string]interface{}
}

type Tracklytics struct {
	superAttrs map[string]interface{}
}

func NewTracklytics() *Tracklytics {
	return &Tracklytics{
		superAttrs: make(map[string]interface{}),
	}
}

func (t *Tracklytics) AddSuperAttribute(key string, value interface{}) {
	t.superAttrs[key] = value
}

func (t *Tracklytics) RemoveSuperAttribute(key string) {
	delete(t.superAttrs, key)
}

func (t *Tracklytics) GetSuperAttributes() map[string]interface{} {
	ret := make(map[string]interface{})
	for k, v := range t.superAttrs {
		ret[k] = v
	}
	return ret
}

func TestAddAndRemoveSuperAttributePublic(t *testing.T) {
	tl := NewTracklytics()
	tl.AddSuperAttribute("pubA", 42)
	if v, ok := tl.GetSuperAttributes()["pubA"]; !ok || v != 42 {
		t.Fatalf("Expected pubA = 42, got %v", tl.GetSuperAttributes())
	}
	tl.RemoveSuperAttribute("pubA")
	if _, ok := tl.GetSuperAttributes()["pubA"]; ok {
		t.Fatalf("pubA should be removed from superAttrs")
	}
}

func TestTrackEventWithSuperAttributesPublic(t *testing.T) {
	tl := NewTracklytics()
	tl.AddSuperAttribute("pubX", 99)
	attrs := map[string]interface{}{"pubY": "fooBar"}
	ev := Event{
		Name: "pEvent", Filters: []int{8}, Tags: []string{"pT"},
		Attributes: attrs, SuperAttributes: tl.GetSuperAttributes(),
	}
	all := make(map[string]interface{})
	for k, v := range ev.Attributes {
		all[k] = v
	}
	for k, v := range ev.SuperAttributes {
		all[k] = v
	}
	if all["pubY"] != "fooBar" || all["pubX"] != 99 {
		t.Fatalf("Expected merged attributes pubY/fooBar, pubX/99; got %v", all)
	}
}