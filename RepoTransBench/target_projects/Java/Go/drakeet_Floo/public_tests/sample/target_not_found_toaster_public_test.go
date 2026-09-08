package sample

import "testing"

type TargetNotFoundToaster struct{}

func (t *TargetNotFoundToaster) OnTargetNotFound(ctx interface{}, uri string, extras map[string]interface{}, flags *int) bool {
	return true
}

func TestOnTargetNotFound_alwaysReturnsTrue_public(t *testing.T) {
	handler := &TargetNotFoundToaster{}
	result := handler.OnTargetNotFound(nil, "another://public-missing", map[string]interface{}{}, nil)
	if !result {
		t.Error("Should always return true")
	}
}