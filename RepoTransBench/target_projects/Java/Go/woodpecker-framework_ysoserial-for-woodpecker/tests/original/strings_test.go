package original

import (
	"testing"
	"sort"
	"strings"
	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestStrings_JoinSimple(t *testing.T) {
	items := []string{"a", "b", "c"}
	assert.Equal(t, "a,b,c", yso.StringsJoin(items, ",", "", ""))
}

func TestStrings_JoinWithPrefixSuffix(t *testing.T) {
	items := []string{"a", "b"}
	assert.Equal(t, "@a@|@b@", yso.StringsJoin(items, "|", "@", "@"))
}

func TestStrings_Repeat(t *testing.T) {
	assert.Equal(t, "aaa", yso.StringsRepeat("a", 3))
	assert.Equal(t, "", yso.StringsRepeat("a", 0))
}

func TestStrings_FormatTable(t *testing.T) {
	rows := [][]string{
		{"ColA", "ColB"},
		{"1", "22"},
		{"333", "4"},
	}
	formatted := yso.StringsFormatTable(rows)
	assert.Equal(t, 3, len(formatted))
	assert.True(t, strings.HasPrefix(formatted[0], "ColA"))
}

func TestStrings_FormatTableMismatchedThrows(t *testing.T) {
	rows := [][]string{
		{"ColA", "ColB"},
		{"1"},
	}
	assert.PanicsWithValue(t, "mismatched number of columns", func() {
		yso.StringsFormatTable(rows)
	})
}

func TestStrings_ToStringComparator(t *testing.T) {
	cmp := yso.ToStringComparator{}
	assert.True(t, cmp.Compare("aaa", "bbb") < 0)
	assert.Equal(t, 0, cmp.Compare("test", "test"))
	assert.True(t, cmp.Compare("zzz", "aaa") > 0)
}