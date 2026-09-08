package original

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
)

type TpsMetric struct {
	ID  string  `json:"id"`
	Min float64 `json:"min"`
	Max float64 `json:"max"`
	Avg float64 `json:"avg"`
	Sum float64 `json:"sum"`
}

func fromJson(jsonStr string) TpsMetric {
	var arr []TpsMetric
	_ = json.Unmarshal([]byte(jsonStr), &arr)
	if len(arr) > 0 {
		return arr[0]
	}
	return TpsMetric{}
}

func TestParseJson(t *testing.T) {
	jsonInput := `[
	{
	"id": "Source__TableSourceScan(table=[[default_catalog__default_database__nexmark]]__fi.numRecordsOutPerSecond",
	"min": 5003.2,
	"max": 5003.2,
	"avg": 5003.2,
	"sum": 10006.3
	}
	]`
	tps := fromJson(jsonInput)
	expected := TpsMetric{
		ID:  "Source__TableSourceScan(table=[[default_catalog__default_database__nexmark]]__fi.numRecordsOutPerSecond",
		Min: 5003.2,
		Max: 5003.2,
		Avg: 5003.2,
		Sum: 10006.3,
	}
	assert.Equal(t, expected, tps)
}