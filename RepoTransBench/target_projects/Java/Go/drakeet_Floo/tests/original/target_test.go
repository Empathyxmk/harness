package original

import "testing"
import "reflect"

type TargetOrig struct {
	Route      string
	TargetClass string
}
func NewTargetOrig(route, targetClass string) *TargetOrig {
	return &TargetOrig{
		Route: route,
		TargetClass: targetClass,
	}
}
func (t *TargetOrig) Equals(o *TargetOrig) bool {
	if o == nil {
		return false
	}
	return t.Route == o.Route && t.TargetClass == o.TargetClass
}

func TestTargetConstructorsAndEquals(t *testing.T) {
	t1 := NewTargetOrig("route", "activity")
	t2 := NewTargetOrig("route", "activity")
	t3 := NewTargetOrig("route2", "activity")
	if t1.Route != "route" {
		t.Error("t1.Route != 'route'")
	}
	if t1.TargetClass != "activity" {
		t.Error("t1.TargetClass != 'activity'")
	}
	if !t1.Equals(t2) {
		t.Error("t1 should equal t2")
	}
	if t1.Equals(t3) {
		t.Error("t1 should not equal t3")
	}
	if t1.Equals(nil) {
		t.Error("t1 should not equal nil")
	}
	if reflect.DeepEqual(t1, &struct{}{}) {
		t.Error("t1 should not be deeply equal to random struct")
	}
	// hashCode analog: compare Go map keys, or leave out.
}