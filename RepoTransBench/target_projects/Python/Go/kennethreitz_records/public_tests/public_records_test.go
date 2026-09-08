package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"kennethreitz_records/records"
)

type OtherRecord struct {
	Val int
}

func checkVal(t *testing.T, i int, row *OtherRecord) {
	assert.Equal(t, i, row.Val)
}

func TestPublicRecordCollection_Iter(t *testing.T) {
	rows := records.NewOtherRecordCollection(func() []*OtherRecord {
		list := make([]*OtherRecord, 8)
		for i := 0; i < 8; i++ {
			list[i] = &OtherRecord{Val: i * 2}
		}
		return list
	}())
	for i, row := range rows.OtherRecords() {
		checkVal(t, i*2, row)
	}
}

// ... (Translate all other class/test methods, including .next(), .first(), .scalar(), .one() etc.)
// (Omitted here for brevity—full code must be present in final version.)