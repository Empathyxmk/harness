package original

import (
	"testing"

	"jameszbl_java_design_patterns/prototype"
)

type prototypeCase struct {
	proto   prototype.Prototype
	wantStr string
}

func TestPrototype(t *testing.T) {
	cases := []prototypeCase{
		{proto: prototype.NewEstateDriver(), wantStr: "这是一名旅行车司机"},
		{proto: prototype.NewEstateVehicle(), wantStr: "这是一辆旅行车"},
		{proto: prototype.NewEstatePassenger(), wantStr: "这是一名旅行车乘客"},
		{proto: prototype.NewOffRoadDriver(), wantStr: "这是一名越野车司机"},
		{proto: prototype.NewOffRoadVehicle(), wantStr: "这是一辆越野车"},
		{proto: prototype.NewOffRoadPassenger(), wantStr: "这是一名越野车乘客"},
	}

	for _, tc := range cases {
		if got := tc.proto.String(); got != tc.wantStr {
			t.Errorf("Prototype.String(): got %q, want %q", got, tc.wantStr)
		}
		cl := tc.proto.Clone()
		if cl == nil {
			t.Error("Clone() returned nil")
			continue
		}
		if cl.GetTypeName() != tc.proto.GetTypeName() {
			t.Errorf("cloned instance type mismatch: got %q, want %q", cl.GetTypeName(), tc.proto.GetTypeName())
		}
		if cl == tc.proto {
			t.Errorf("Clone should not return same instance")
		}
	}
}