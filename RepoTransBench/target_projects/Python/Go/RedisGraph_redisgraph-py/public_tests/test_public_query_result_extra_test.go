package public_tests

import (
	"testing"

	"redisgraph/query_result"

	"github.com/stretchr/testify/assert"
)

func TestPublicQueryResultScalarAccess(t *testing.T) {
	qr := query_result.NewQueryResultWithHeaderRecords(
		[]string{"foo", "bar"}, [][]interface{}{{5, "abc"}, {6, "xyz"}},
	)
	assert.Equal(t, []string{"foo", "bar"}, qr.Header)
	assert.Equal(t, "xyz", qr.Records[1][1])
}

func TestPublicQueryResultToDicts(t *testing.T) {
	qr := query_result.NewQueryResultWithHeaderRecords(
		[]string{"a", "b"}, [][]interface{}{{10, 20}, {30, 40}},
	)
	dicts := qr.ToDicts()
	assert.Equal(t, []map[string]interface{}{
		{"a": 10, "b": 20},
		{"a": 30, "b": 40},
	}, dicts)
}

func TestPublicQueryResultUpdateRecords(t *testing.T) {
	qr := query_result.NewQueryResultWithHeaderRecords(
		[]string{"c"}, [][]interface{}{{123}},
	)
	qr.Records = append(qr.Records, []interface{}{456})
	assert.Equal(t, 2, len(qr.Records))
	assert.Equal(t, 456, qr.Records[len(qr.Records)-1][0])
}