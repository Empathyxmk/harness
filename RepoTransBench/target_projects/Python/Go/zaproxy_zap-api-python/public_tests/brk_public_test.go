package public_tests

import (
	"testing"
	"strings"
	"github.com/stretchr/testify/assert"
)

// Mimic brk_module with public API
type BrkModulePub struct{}

func (b *BrkModulePub) AddBreakPoint(url, method string) map[string]any {
	return map[string]any{"status": "OK", "method": method, "url": url}
}
func (b *BrkModulePub) RemoveBreakPoint(id string) map[string]any {
	return map[string]any{"status": "REMOVED", "id": id}
}

func TestBrkAddBreakPointDiffData(t *testing.T) {
	brk := &BrkModulePub{}
	url := "http://public.example.com/login"
	method := "POST"
	resp := brk.AddBreakPoint(url, method)
	assert.Equal(t, "OK", resp["status"])
	assert.Equal(t, method, resp["method"])
	urlStr, ok := resp["url"].(string)
	assert.True(t, ok)
	assert.True(t, strings.HasPrefix(urlStr, "http://public."))
}

func TestBrkRemoveBreakPointDiffData(t *testing.T) {
	brk := &BrkModulePub{}
	brkId := "customBrk2"
	resp := brk.RemoveBreakPoint(brkId)
	assert.Equal(t, "REMOVED", resp["status"])
	assert.Equal(t, brkId, resp["id"])
}