package original

import (
	"testing"
	"fmt"
)

// Note: The real implementation would parse and create ParamSpec objects as in parser_test.py, but we're mocking here.

func TestSplitParam(t *testing.T) {
	cases := []struct {
		input string
		want  *ParamSpec
	}{
		{"_", &ParamSpec{Var: "_"}},
		{"_.version", &ParamSpec{Var: "_", Member: stringPtr("version")}},
		{"_.version:02d", &ParamSpec{Var: "_", Member: stringPtr("version"), Format: stringPtr("02d")}},
		{"_.file[1:5]", &ParamSpec{Var: "_", Member: stringPtr("file"), StringSlice: &Slice{Start: intPtr(1), End: intPtr(5)}}},
		{"_.file[1:5]:01", &ParamSpec{Var: "_", Member: stringPtr("file"), StringSlice: &Slice{Start: intPtr(1), End: intPtr(5)}, Format: stringPtr("01")}},
		{"param", &ParamSpec{Var: "param"}},
		{"param:-<2", &ParamSpec{Var: "param", Format: stringPtr("-<2")}},
		{"param[1]:-<2", &ParamSpec{Var: "param", StringSlice: &Slice{Start: intPtr(1), End: intPtr(2)}, Format: stringPtr("-<2")}},
		{"param[-1:]", &ParamSpec{Var: "param", StringSlice: &Slice{Start: intPtr(-1), End: nil}}},
		{"param[:-3]", &ParamSpec{Var: "param", StringSlice: &Slice{Start: nil, End: intPtr(-3)}}},
	}

	for _, c := range cases {
		got := ParamSpecFromString(c.input)
		if got == nil || !got.Equal(*c.want) {
			t.Errorf("ParamSpecFromString(%q): want %#v, got %#v", c.input, c.want, got)
		}
	}
}

func TestSliceParsing(t *testing.T) {
	valid := []struct {
		input string
		want  *ParamSpec
	}{
		{"p[0]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: intPtr(0), End: intPtr(1)}}},
		{"p[:5]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: nil, End: intPtr(5)}}},
		{"p[6:]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: intPtr(6), End: nil}}},
		{"p[5:6]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: intPtr(5), End: intPtr(6)}}},
		{"p[:-1]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: nil, End: intPtr(-1)}}},
		{"p[1:-2]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: intPtr(1), End: intPtr(-2)}}},
	}
	for _, c := range valid {
		got := ParamSpecFromString(c.input)
		if got == nil || !got.Equal(*c.want) {
			t.Errorf("ParamSpecFromString(%q): want %#v, got %#v", c.input, c.want, got)
		}
	}

	meaningless := []struct {
		input string
		want  *ParamSpec
	}{
		{"p[:]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: nil, End: nil}}},
		{"p[-5:5]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: intPtr(-5), End: intPtr(5)}}},
		{"p[11:5]", &ParamSpec{Var: "p", StringSlice: &Slice{Start: intPtr(11), End: intPtr(5)}}},
	}
	for _, c := range meaningless {
		got := ParamSpecFromString(c.input)
		if got == nil || !got.Equal(*c.want) {
			t.Errorf("ParamSpecFromString(%q): want %#v, got %#v", c.input, c.want, got)
		}
	}

	bad := []string{
		"p[]", "p[a]", "p[a:b]", "p[:b]", "p[1:3:2]", "p[::]",
	}
	for _, s := range bad {
		got := ParamSpecFromString(s)
		if got != nil {
			t.Errorf("ParamSpecFromString(%q): expected nil, got %#v", s, got)
		}
	}
}

func TestSplitExampleStrings(t *testing.T) {
	cases := []struct {
		input string
		want  *ParamSpec
	}{
		{"d1:.3f", &ParamSpec{Var: "d1", Format: stringPtr(".3f")}},
		{"d1.unit", &ParamSpec{Var: "d1", Member: stringPtr("unit")}},
		{"d1:03.0f", &ParamSpec{Var: "d1", Format: stringPtr("03.0f")}},
		{"width:.0f", &ParamSpec{Var: "width", Format: stringPtr(".0f")}},
		{"width.expr", &ParamSpec{Var: "width", Member: stringPtr("expr")}},
		{"height.expr", &ParamSpec{Var: "height", Member: stringPtr("expr")}},
		{"_.version", &ParamSpec{Var: "_", Member: stringPtr("version")}},
		{"_.version:03", &ParamSpec{Var: "_", Member: stringPtr("version"), Format: stringPtr("03")}},
		{"_.file", &ParamSpec{Var: "_", Member: stringPtr("file")}},
		{"_.component", &ParamSpec{Var: "_", Member: stringPtr("component")}},
		{"_.date", &ParamSpec{Var: "_", Member: stringPtr("date")}},
		{"_.date:%m/%d/%Y", &ParamSpec{Var: "_", Member: stringPtr("date"), Format: stringPtr("%m/%d/%Y")}},
		{"_.date:%U", &ParamSpec{Var: "_", Member: stringPtr("date"), Format: stringPtr("%U")}},
		{"_.date:%W", &ParamSpec{Var: "_", Member: stringPtr("date"), Format: stringPtr("%W")}},
		{"_.date:%H:%M", &ParamSpec{Var: "_", Member: stringPtr("date"), Format: stringPtr("%H:%M")}},
	}
	for _, c := range cases {
		got := ParamSpecFromString(c.input)
		if got == nil || !got.Equal(*c.want) {
			t.Errorf("ParamSpecFromString(%q): want %#v, got %#v", c.input, c.want, got)
		}
	}
}

func TestBadParamString(t *testing.T) {
	badStrings := []string{
		"",
		".",
		".a",
		"a.",
		".a[10]",
		".a:5",
		".[]",
		"a[]",
		"[]",
		":",
		"a[",
		"a]",
		"[1]",
		"a[1",
		":5",
		"a[10:10][]",
	}
	for _, bad := range badStrings {
		if ParamSpecFromString(bad) != nil {
			t.Errorf("ParamSpecFromString(%q): expected nil", bad)
		}
	}
}