package public_tests

import (
	"reflect"
	"regexp"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func parseFloat(val string) float64 {
	re := regexp.MustCompile(`-?[\d\.,]+`)
	found := re.FindString(val)
	found = strings.ReplaceAll(found, ".", "")
	found = strings.ReplaceAll(found, ",", ".")
	f, _ := strconv.ParseFloat(found, 64)
	return f
}

func parseGenericTransaction(tx map[string]interface{}) map[string]interface{} {
	newTx := make(map[string]interface{})
	for k, v := range tx {
		newTx[k] = v
	}
	val, ok := tx["amount"].(string)
	if ok {
		newTx["amount"] = parseFloat(val)
	}
	return newTx
}

func TestParseFloatPublic(t *testing.T) {
	assert.Equal(t, 1234.56, parseFloat("1234,56"))
	assert.Equal(t, 0.0, parseFloat("0,00"))
	assert.Equal(t, -76.54, parseFloat("-76,54"))
}

func TestParseGenericTransactionPublic(t *testing.T) {
	txn := map[string]interface{}{"amount": "99,99", "description": "Check parsing public"}
	parsed := parseGenericTransaction(txn)
	assert.True(t, reflect.DeepEqual(parsed["amount"], 99.99))
	assert.Equal(t, "Check parsing public", parsed["description"])
}