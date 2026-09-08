package original

import (
	"testing"
	"jameszbl_java_design_patterns/decorator"
)

func TestHammerSmithOperations(t *testing.T) {
	base := decorator.NewCarpenterOperationWithSpy()
	hammerSmith := decorator.NewHammerSmithOperation(base)

	hammerSmith.CheckBefore()
	if base.CheckBeforeCount() != 1 {
		t.Errorf("base.CheckBefore called %d times, want 1", base.CheckBeforeCount())
	}

	hammerSmith.Join()
	if base.JoinCount() != 1 {
		t.Errorf("base.Join called %d times, want 1", base.JoinCount())
	}

	hammerSmith.CheckAfter()
	if base.CheckAfterCount() != 1 {
		t.Errorf("base.CheckAfter called %d times, want 1", base.CheckAfterCount())
	}
}