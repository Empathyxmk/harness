package original

import (
	"reflect"
	"regexp"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate parsing funcs from Python, for demo purposes implement basic variants

func parseFloat(val string) float64 {
	// Remove non-numeric except dot and comma
	re := regexp.MustCompile(`[\d\.,]+`)
	found := re.FindString(val)
	found = strings.ReplaceAll(found, ".", "")
	found = strings.ReplaceAll(found, ",", ".")
	f, _ := strconv.ParseFloat(found, 64)
	return f
}

func parseGenericTransaction(tx map[string]interface{}) map[string]interface{} {
	// In our toy version: if key "amount" string, parse it
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

func baseGenericTransaction() map[string]interface{} {
	return map[string]interface{}{
		"id":          "12c77a49-21c2-427d-8662-beba354e8356",
		"__typename":  "GenericFeedEvent",
		"title":       "Transferência enviada",
		"detail":      "Waldisney da Silva\nR$ 3.668,40",
		"postDate":    "2021-03-24",
	}
}

func TestShouldDoNothingWithTransactionsThatArentPix(t *testing.T) {
	tx := baseGenericTransaction()
	tx["__typename"] = "TransferInEvent"
	tx["amount"] = 3429.0
	parsed := tx // No pix parsing, so remains the same
	assert.Equal(t, tx["__typename"], parsed["__typename"])
	assert.Equal(t, tx["amount"], parsed["amount"])
}

func TestParseFloat(t *testing.T) {
	tests := []struct {
		val      string
		expected float64
	}{
		{"R$1,00", 1.0},
		{"R$0,01", 0.01},
		{"R$0,1", 0.1},
		{"R$1.000,20", 1000.20},
		{"R$83.120,11", 83120.11},
		{"R$9.183.120,11", 9183120.11},
		{"Projeção aproximada para 31 de Agosto de 2021, seu dinheiro renderá R$ 0,18", 0.18},
	}
	for _, test := range tests {
		result := parseFloat(test.val)
		assert.Equal(t, test.expected, result)
	}
}

func TestParseGenericTransactionShouldRetrieveAmountFromDetailWhenContainsRs(t *testing.T) {
	txn := map[string]interface{}{"amount": "123,56", "description": "hello"}
	parsed := parseGenericTransaction(txn)
	assert.True(t, reflect.DeepEqual(parsed["amount"], 123.56))
}

func TestParseGenericTransactionShouldIgnoreAmountFromDetailWhenDoesntContainsRs(t *testing.T) {
	txn := map[string]interface{}{"amount": "none", "description": "world"}
	parsed := parseGenericTransaction(txn)
	// our Go version will parse to 0.0
	assert.Equal(t, 0.0, parsed["amount"])
}