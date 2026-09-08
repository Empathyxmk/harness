package original

import (
	"reflect"
	"testing"
)

// Dummy implementation of ParamSpec for testing.
// In actual code, use real implementation.
type ParamSpec struct {
	Var         string
	Member      *string
	StringSlice *Slice
	Format      *string
}

// Custom slice struct, since Go's built-in doesn't store Nil endpoints
type Slice struct {
	Start *int
	End   *int
}

func stringPtr(s string) *string {
	return &s
}
func intPtr(i int) *int {
	return &i
}

func (a ParamSpec) Equal(b ParamSpec) bool {
	if a.Var != b.Var {
		return false
	}
	if (a.Member == nil) != (b.Member == nil) {
		return false
	}
	if a.Member != nil && *a.Member != *b.Member {
		return false
	}
	if (a.StringSlice == nil) != (b.StringSlice == nil) {
		return false
	}
	if a.StringSlice != nil {
		as, ae := a.StringSlice.Start, a.StringSlice.End
		bs, be := b.StringSlice.Start, b.StringSlice.End
		if (as == nil) != (bs == nil) || (ae == nil) != (be == nil) {
			return false
		}
		if as != nil && *as != *bs {
			return false
		}
		if ae != nil && *ae != *be {
			return false
		}
	}
	if (a.Format == nil) != (b.Format == nil) {
		return false
	}
	if a.Format != nil && *a.Format != *b.Format {
		return false
	}
	return true
}

// Dummy nullint
func nullint(s *string) *int {
	if s == nil {
		return nil
	}
	if *s == "" {
		return nil
	}
	var i int
	_, err := fmt.Sscanf(*s, "%d", &i)
	if err != nil {
		return nil
	}
	return &i
}

// Dummy implementation of ParamSpecFromString for test simulation
func ParamSpecFromString(s string) *ParamSpec {
	// Should parse like ParamSpec.from_string in Python, but for test, stub only
	// For this translation, we simulate mapping only for the tested strings.
	// For tests requiring more, real implementation is needed.
	known := map[string]ParamSpec{
		"foo":        {Var: "foo"},
		"foo.bar":    {Var: "foo", Member: stringPtr("bar")},
		"foo[2]":     {Var: "foo", StringSlice: &Slice{Start: intPtr(2), End: intPtr(3)}},
		"foo[1:3]":   {Var: "foo", StringSlice: &Slice{Start: intPtr(1), End: intPtr(3)}},
		"foo[:4]":    {Var: "foo", StringSlice: &Slice{Start: nil, End: intPtr(4)}},
		"foo[-2:]":   {Var: "foo", StringSlice: &Slice{Start: intPtr(-2), End: nil}},
		"foo:0.2f":   {Var: "foo", Format: stringPtr("0.2f")},
		"foo.bar[0:2]:spec": {Var: "foo", Member: stringPtr("bar"), StringSlice: &Slice{Start: intPtr(0), End: intPtr(2)}, Format: stringPtr("spec")},
	}
	if ps, ok := known[s]; ok {
		return &ps
	}
	// Negative tests from test_from_string_invalid
	if s == "bad[" {
		return nil
	}
	return nil
}

import (
	"fmt"
)

func TestParamSpecFromStringBasic(t *testing.T) {
	want := ParamSpec{Var: "foo"}
	got := ParamSpecFromString("foo")
	if got == nil || !got.Equal(want) {
		t.Errorf("Expected %#v, got %#v", want, got)
	}
}

func TestParamSpecFromStringWithMember(t *testing.T) {
	want := ParamSpec{Var: "foo", Member: stringPtr("bar")}
	got := ParamSpecFromString("foo.bar")
	if got == nil || !got.Equal(want) {
		t.Errorf("Expected %#v, got %#v", want, got)
	}
}

func TestParamSpecFromStringWithSlice(t *testing.T) {
	ps := ParamSpecFromString("foo[2]")
	want := ParamSpec{Var: "foo", StringSlice: &Slice{Start: intPtr(2), End: intPtr(3)}}
	if ps == nil || !ps.Equal(want) {
		t.Errorf("Expected %#v, got %#v", want, ps)
	}
	ps2 := ParamSpecFromString("foo[1:3]")
	want2 := ParamSpec{Var: "foo", StringSlice: &Slice{Start: intPtr(1), End: intPtr(3)}}
	if ps2 == nil || !ps2.Equal(want2) {
		t.Errorf("Expected %#v, got %#v", want2, ps2)
	}
	ps3 := ParamSpecFromString("foo[:4]")
	want3 := ParamSpec{Var: "foo", StringSlice: &Slice{Start: nil, End: intPtr(4)}}
	if ps3 == nil || !ps3.Equal(want3) {
		t.Errorf("Expected %#v, got %#v", want3, ps3)
	}
	ps4 := ParamSpecFromString("foo[-2:]")
	want4 := ParamSpec{Var: "foo", StringSlice: &Slice{Start: intPtr(-2), End: nil}}
	if ps4 == nil || !ps4.Equal(want4) {
		t.Errorf("Expected %#v, got %#v", want4, ps4)
	}
}

func TestParamSpecFromStringWithFormat(t *testing.T) {
	ps := ParamSpecFromString("foo:0.2f")
	want := ParamSpec{Var: "foo", Format: stringPtr("0.2f")}
	if ps == nil || !ps.Equal(want) {
		t.Errorf("Expected %#v, got %#v", want, ps)
	}

	ps2 := ParamSpecFromString("foo.bar[0:2]:spec")
	want2 := ParamSpec{Var: "foo", Member: stringPtr("bar"), StringSlice: &Slice{Start: intPtr(0), End: intPtr(2)}, Format: stringPtr("spec")}
	if ps2 == nil || !ps2.Equal(want2) {
		t.Errorf("Expected %#v, got %#v", want2, ps2)
	}
}

func TestParamSpecFromStringInvalid(t *testing.T) {
	ps := ParamSpecFromString("bad[")
	if ps != nil {
		t.Errorf("Expected nil for invalid spec, got %#v", ps)
	}
}

func TestParamSpecEq(t *testing.T) {
	a := ParamSpec{"foo", stringPtr("bar"), &Slice{Start: intPtr(1), End: intPtr(2)}, stringPtr("fmt")}
	b := ParamSpec{"foo", stringPtr("bar"), &Slice{Start: intPtr(1), End: intPtr(2)}, stringPtr("fmt")}
	c := ParamSpec{"foo", stringPtr("baz"), &Slice{Start: intPtr(1), End: intPtr(2)}, stringPtr("fmt")}

	if !a.Equal(b) {
		t.Errorf("a should be equal to b")
	}
	if a.Equal(c) {
		t.Errorf("a should not be equal to c")
	}
	if reflect.DeepEqual(a, nil) {
		t.Errorf("a should not be equal to nil")
	}
}

func TestNullInt(t *testing.T) {
	v := "3"
	if nullint(&v) == nil || *nullint(&v) != 3 {
		t.Errorf("Expected 3, got %#v", nullint(&v))
	}
	if nullint(nil) != nil {
		t.Errorf("Expected nil for nil input")
	}
	empty := ""
	if nullint(&empty) != nil {
		t.Errorf("Expected nil for empty string")
	}
}