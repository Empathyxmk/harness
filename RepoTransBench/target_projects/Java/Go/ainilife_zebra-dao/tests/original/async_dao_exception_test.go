package original

import (
	"testing"
)

func TestAsyncDaoException_Message(t *testing.T) {
	ex := AsyncDaoException{"msg"}
	if ex.Error() != "msg" {
		t.Errorf("expected 'msg', got %v", ex.Error())
	}
}