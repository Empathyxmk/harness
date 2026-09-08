package original

import (
	"testing"
	"opengamma_elsql/tests"
)

type ContainerSqlFragment struct {
	fragments []tests.DummySqlFragment
}

func (c *ContainerSqlFragment) AddFragment(frag tests.DummySqlFragment) {
	c.fragments = append(c.fragments, frag)
}

func (c *ContainerSqlFragment) GetFragments() []tests.DummySqlFragment {
	return c.fragments
}

func (c *ContainerSqlFragment) ToSQL(buf *tests.StringBuilder, fragments, params interface{}, loopIndex []int) {
	for _, frag := range c.fragments {
		frag.ToSQL(buf, fragments, params, loopIndex)
	}
}

func (c *ContainerSqlFragment) String() string {
	s := "["
	for i, frag := range c.fragments {
		if i > 0 {
			s += ", "
		}
		s += frag.String()
	}
	s += "]"
	return s
}

func TestContainerSqlFragment_AddAndGetFragments(t *testing.T) {
	c := &ContainerSqlFragment{}
	frag1 := tests.DummySqlFragment{Tag: "a"}
	frag2 := tests.DummySqlFragment{Tag: "b"}
	c.AddFragment(frag1)
	c.AddFragment(frag2)
	frags := c.GetFragments()
	if len(frags) != 2 {
		t.Errorf("expected 2 fragments, got %d", len(frags))
	}
	found := false
	for _, f := range frags {
		if f.String() == frag1.String() {
			found = true
		}
	}
	if !found {
		t.Errorf("expected fragments to contain frag1")
	}
}

func TestContainerSqlFragment_ToSQLCallsChildren(t *testing.T) {
	c := &ContainerSqlFragment{}
	c.AddFragment(tests.DummySqlFragment{Tag: "X"})
	c.AddFragment(tests.DummySqlFragment{Tag: "Y"})
	buf := &tests.StringBuilder{}
	c.ToSQL(buf, nil, nil, []int{})
	if buf.String() != "XY" {
		t.Errorf("expected 'XY', got '%s'", buf.String())
	}
}

func TestContainerSqlFragment_ToStringFormat(t *testing.T) {
	c := &ContainerSqlFragment{}
	c.AddFragment(tests.DummySqlFragment{Tag: "X"})
	if s := c.String(); !contains(s, "X") {
		t.Errorf("expected toString() to contain 'X', got %s", s)
	}
}

func contains(str, substr string) bool {
	return len(str) >= len(substr) && (str == substr || (len(str) > len(substr) && (str[1:] == substr || contains(str[1:], substr))))
}