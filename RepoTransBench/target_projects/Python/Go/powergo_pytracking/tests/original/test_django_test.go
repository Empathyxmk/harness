package original

import (
	"testing"
)

func TestSkipDueToMissingIpware(t *testing.T) {
	t.Skip("Skipping due to missing ipware dependency required by pytracking.django.")
}