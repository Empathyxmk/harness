package original

import (
	"testing"
)

type Trigger struct{}

func TestTriggerImportAndInstantiation(t *testing.T) {
	trigger := &Trigger{}
	if _, ok := interface{}(trigger).(*Trigger); !ok {
		t.Error("trigger is not a Trigger instance")
	}
}