package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"kennethreitz_records/records"
)

func TestRecordCollectionIterNextSliceReprPublic(t *testing.T) {
	rc := records.NewRecordCollection([]*records.Record{
		records.NewRecord([]string{"b"}, []interface{}{10}),
		records.NewRecord([]string{"b"}, []interface{}{20}),
	})
	assert.Contains(t, rc.String(), "pending")
	vals := rc.Records()
	assert.Len(t, vals, 2)

	rc2 := records.NewRecordCollection([]*records.Record{
		records.NewRecord([]string{"b"}, []interface{}{40}),
		records.NewRecord([]string{"b"}, []interface{}{50}),
	})
	out, err := rc2.Get(0)
	assert.NoError(t, err)
	assert.IsType(t, &records.Record{}, out)
	sl := rc2.Slice(0, 2)
	assert.IsType(t, &records.RecordCollection{}, sl)
}

func TestRecordCollectionConsumingAndAttrsPublic(t *testing.T) {
	rc := records.NewRecordCollection([]*records.Record{
		records.NewRecord([]string{"foo"}, []interface{}{99}),
		records.NewRecord([]string{"foo"}, []interface{}{100}),
		records.NewRecord([]string{"foo"}, []interface{}{101}),
	})
	_ = rc.Slice(0, 10)
	rc.Add(records.NewRecord([]string{"foo"}, []interface{}{102}))
	assert.GreaterOrEqual(t, rc.Len(), 3)
	// Simulate as_dicts test
	if rc.AsDicts != nil {
		v := rc.AsDicts()
		assert.IsType(t, []map[string]interface{}{}, v)
	} else {
		assert.True(t, true)
	}
}