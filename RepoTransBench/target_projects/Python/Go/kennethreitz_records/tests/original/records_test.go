package original

import (
	"errors"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
	"kennethreitz_records/records"
)

type IdRecord struct {
	Id int
}

func checkID(t *testing.T, i int, row *IdRecord) {
	assert.Equal(t, i, row.Id, "IdRecord mismatch: got %#v want %d", row, i)
}

func TestRecordCollectionIter(t *testing.T) {
	gen := func() []*IdRecord {
		var res []*IdRecord
		for i := 0; i < 10; i++ {
			res = append(res, &IdRecord{Id: i})
		}
		return res
	}
	rows := records.NewRecordCollectionFromIdRecord(gen())
	for i, row := range rows.IDRecords() {
		checkID(t, i, row)
	}
}

func TestRecordCollectionNext(t *testing.T) {
	gen := func() []*IdRecord {
		var res []*IdRecord
		for i := 0; i < 10; i++ {
			res = append(res, &IdRecord{Id: i})
		}
		return res
	}
	rows := records.NewRecordCollectionFromIdRecord(gen())
	for i := 0; i < 10; i++ {
		checkID(t, i, rows.NextIDRecord())
	}
}

func TestRecordCollectionIterAndNext(t *testing.T) {
	gen := func() []*IdRecord {
		var res []*IdRecord
		for i := 0; i < 10; i++ {
			res = append(res, &IdRecord{Id: i})
		}
		return res
	}
	rows := records.NewRecordCollectionFromIdRecord(gen())
	iter := rows.Iterator()
	i, row := iter.NextIDRecord()
	checkID(t, i, row)
	rows.NextIDRecord() // Cache second row
	i, row = iter.NextIDRecord()
	checkID(t, i, row)
}

func TestRecordCollectionMultipleIter(t *testing.T) {
	gen := func() []*IdRecord {
		var res []*IdRecord
		for i := 0; i < 10; i++ {
			res = append(res, &IdRecord{Id: i})
		}
		return res
	}
	rows := records.NewRecordCollectionFromIdRecord(gen())
	i := rows.Iterator()
	j := rows.Iterator()
	idx, row := i.NextIDRecord()
	checkID(t, idx, row)
	idx, row = j.NextIDRecord()
	checkID(t, idx, row)
	idx, row = j.NextIDRecord()
	checkID(t, idx, row)
	idx, row = i.NextIDRecord()
	checkID(t, idx, row)
}

func TestRecordCollectionSliceIter(t *testing.T) {
	gen := func() []*IdRecord {
		var res []*IdRecord
		for i := 0; i < 10; i++ {
			res = append(res, &IdRecord{Id: i})
		}
		return res
	}
	rows := records.NewRecordCollectionFromIdRecord(gen())
	for i, row := range rows.Slice(0, 5).IDRecords() {
		checkID(t, i, row)
	}
	for i, row := range rows.IDRecords() {
		checkID(t, i, row)
	}
	assert.Equal(t, 10, rows.Len())
}

func TestRecordCollectionAllReturnsAListOfRecords(t *testing.T) {
	gen := func() []*IdRecord {
		var res []*IdRecord
		for i := 0; i < 3; i++ {
			res = append(res, &IdRecord{Id: i})
		}
		return res
	}
	rows := records.NewRecordCollectionFromIdRecord(gen())
	want := []*IdRecord{{Id: 0}, {Id: 1}, {Id: 2}}
	got := rows.AllIDRecords()
	assert.True(t, reflect.DeepEqual(want, got), "All() mismatch: got %#v want %#v", got, want)
}

func TestRecordCollectionFirstReturnsASingleRecord(t *testing.T) {
	gen := func() []*IdRecord { return []*IdRecord{{Id: 0}} }
	rows := records.NewRecordCollectionFromIdRecord(gen())
	first := rows.FirstIDRecord()
	assert.True(t, first != nil && first.Id == 0)
}

func TestRecordCollectionFirstDefaultsToNil(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	first := rows.FirstIDRecord()
	assert.Nil(t, first)
}

func TestRecordCollectionFirstDefaultIsOverridable(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	got := rows.FirstOr("Cheese")
	assert.Equal(t, "Cheese", got)
}

func TestRecordCollectionFirstRaisesDefaultIfItsAnErrorType(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	cheeseErr := errors.New("cheese error")
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic") // like raises in pytest
		}
	}()
	rows.FirstOrPanic(cheeseErr)
}

func TestRecordCollectionFirstRaisesDefaultIfItsAnErrorValue(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	cheeseErr := errors.New("cheddar")
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic")
		}
	}()
	rows.FirstOrPanic(cheeseErr)
}

func TestRecordCollectionOneReturnsASingleRecord(t *testing.T) {
	gen := func() []*IdRecord { return []*IdRecord{{Id: 0}} }
	rows := records.NewRecordCollectionFromIdRecord(gen())
	one := rows.OneIDRecord()
	assert.True(t, one != nil && one.Id == 0)
}

func TestRecordCollectionOneDefaultsToNil(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	one := rows.OneIDRecord()
	assert.Nil(t, one)
}

func TestRecordCollectionOneDefaultIsOverridable(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	got := rows.OneOr("Cheese")
	assert.Equal(t, "Cheese", got)
}

func TestRecordCollectionOneRaisesWhenMoreThanOne(t *testing.T) {
	gen := func() []*IdRecord { return []*IdRecord{{Id: 0}, {Id: 1}, {Id: 2}} }
	rows := records.NewRecordCollectionFromIdRecord(gen())
	assert.Panics(t, func() { rows.OneIDRecord() })
}

func TestRecordCollectionOneRaisesDefaultIfItsAnErrorType(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	rabbitErr := errors.New("rabbit error")
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic")
		}
	}()
	rows.OneOrPanic(rabbitErr)
}

func TestRecordCollectionOneRaisesDefaultIfItsAnErrorInstance(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	rabbitErr := errors.New("lop")
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic")
		}
	}()
	rows.OneOrPanic(rabbitErr)
}

func TestRecordCollectionScalarReturnsASingleRecord(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{{Id: 0}})
	sc := rows.Scalar()
	assert.Equal(t, 0, sc)
}

func TestRecordCollectionScalarDefaultsToNil(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	sc := rows.ScalarOrNil()
	assert.Nil(t, sc)
}

func TestRecordCollectionScalarDefaultIsOverridable(t *testing.T) {
	rows := records.NewRecordCollectionFromIdRecord([]*IdRecord{})
	assert.Equal(t, "Kaffe", rows.ScalarOr("Kaffe"))
}

func TestRecordCollectionScalarRaisesWhenMoreThanOne(t *testing.T) {
	gen := func() []*IdRecord { return []*IdRecord{{Id: 0}, {Id: 1}, {Id: 2}} }
	rows := records.NewRecordCollectionFromIdRecord(gen())
	assert.Panics(t, func() { rows.Scalar() })
}

func TestRecordDir(t *testing.T) {
	keys := []string{"id", "name", "email"}
	values := []interface{}{1, "", ""}
	rec := records.NewRecord(keys, values)
	_dir := rec.Keys()
	for _, key := range keys {
		assert.Contains(t, _dir, key)
	}
	baseFields := records.BaseObjectFields()
	for _, key := range baseFields {
		assert.Contains(t, _dir, key)
	}
}

func TestRecordDuplicateColumn(t *testing.T) {
	keys := []string{"id", "name", "email", "email"}
	values := []interface{}{1, "", "", ""}
	rec := records.NewRecord(keys, values)
	_, err := rec.Get("email")
	assert.Error(t, err)
}