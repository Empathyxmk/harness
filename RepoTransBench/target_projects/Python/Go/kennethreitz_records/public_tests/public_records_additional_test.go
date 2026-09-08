package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"kennethreitz_records/records"
)

func TestRecordReprAndExportPublic(t *testing.T) {
	rec := records.NewRecord([]string{"r", "s"}, []interface{}{3, "abc"})
	rep := rec.Repr()
	assert.True(t, strings.HasPrefix(rep, "<Record"))
	exported, err := rec.Export("json")
	assert.NoError(t, err)
	assert.Contains(t, exported, "\"abc\"")
}

func TestRecordAsDictOrderedPublic(t *testing.T) {
	rec := records.NewRecord([]string{"z", "x", "y"}, []interface{}{7, 8, 9})
	d1 := rec.AsDict() // returns map[string]interface{}
	d2 := rec.AsOrderedDict() // returns ordered map (slice of keys + map)
	assert.IsType(t, map[string]interface{}{}, d1)
	keys := d2.Keys()
	expOrder := []string{"z", "x", "y"}
	assert.EqualValues(t, expOrder, keys)
}

func TestRecordGetMethodPublic(t *testing.T) {
	rec := records.NewRecord([]string{"foo", "bar"}, []interface{}{5, 6})
	val, ok := rec.Get("foo")
	assert.True(t, ok)
	assert.Equal(t, 5, val)
	val, ok = rec.GetDefault("baz", 99)
	assert.True(t, ok)
	assert.Equal(t, 99, val)
}

func TestRecordCollectionCSVExportPublic(t *testing.T) {
	rc := records.NewRecordCollection([]*records.Record{
		records.NewRecord([]string{"id", "val"}, []interface{}{5, "a"}),
		records.NewRecord([]string{"id", "val"}, []interface{}{6, "b"}),
	})
	csv, err := rc.Export("csv")
	if err != nil {
		t.Skip("Tablib/export or CSV format missing")
	}
	assert.IsType(t, "", csv)
	assert.Contains(t, csv, "id")
}

func TestRecordCollectionExportXlsxPublic(t *testing.T) {
	rc := records.NewRecordCollection([]*records.Record{
		records.NewRecord([]string{"num"}, []interface{}{111}),
		records.NewRecord([]string{"num"}, []interface{}{222}),
	})
	data, err := rc.Export("xlsx")
	if err != nil {
		t.Skip("Tablib/xlsx not present or export fails")
	}
	assert.True(t, isBytesOrString(data))
}

func isBytesOrString(x interface{}) bool {
	switch x.(type) {
	case []byte, string:
		return true
	default:
		return false
	}
}

func TestIsExceptionCasesPublic(t *testing.T) {
	ok := records.IsException(func() error {
		return &CustomError{}
	})
	assert.True(t, ok)
	ok = records.IsException(CustomError{})
	assert.True(t, ok)
	ok = records.IsException(&CustomError{})
	assert.True(t, ok)
}

type CustomError struct{}

func (e CustomError) Error() string { return "custom error" }

func TestRecordCollectionReprAsciiPendingPublic(t *testing.T) {
	rc := records.NewRecordCollection([]*records.Record{
		records.NewRecord([]string{"w", "x"}, []interface{}{11, 22}),
		records.NewRecord([]string{"w", "x"}, []interface{}{33, 44}),
	})
	r := rc.String()
	assert.True(t, strings.HasPrefix(r, "<RecordCollection"))
}

func TestRecordAsDictKeysMatchPublic(t *testing.T) {
	rec := records.NewRecord([]string{"a", "b", "c"}, []interface{}{1, 2, 3})
	asdict := rec.AsDict()
	for _, k := range []string{"a", "b", "c"} {
		_, ok := asdict[k]
		assert.True(t, ok)
	}
}

func TestRecordExportDatasetPublic(t *testing.T) {
	rec := records.NewRecord([]string{"val"}, []interface{}{898})
	ds := rec.Dataset()
	assert.NotNil(t, ds.Headers)
	assert.Contains(t, ds.Headers, "val")
}