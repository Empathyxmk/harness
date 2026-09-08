package original

import (
	"testing"

	"redisgraph/query_result"

	"github.com/stretchr/testify/assert"
)

type DummyResultSet struct {
	results [][]interface{}
	header  []string
	index   int
}

func NewDummyResultSet() *DummyResultSet {
	return &DummyResultSet{
		results: [][]interface{}{
			{"a", "b"},
			{1, 2},
			{3, 4},
		},
		header: []string{"a", "b"},
		index:  -1,
	}
}

func (d *DummyResultSet) Next() bool {
	d.index++
	return d.index < len(d.results)-1
}

func TestQueryResultBasicMethods(t *testing.T) {
	rs := NewDummyResultSet()
	qr := query_result.NewQueryResult(rs)
	assert.NotNil(t, qr)
	qr.Header = []struct {
		Col  string
		Type string
	}{{"col", "type"}}
	assert.Equal(t, []string{"col"}, qr.Keys())
	qr.Position = 0
	assert.True(t, qr.Next())
	assert.NotNil(t, qr)
}

func TestQueryResultStrAndRepr(t *testing.T) {
	rs := NewDummyResultSet()
	qr := query_result.NewQueryResult(rs)
	assert.IsType(t, "", qr.String())
	assert.IsType(t, "", qr.GoString())
}