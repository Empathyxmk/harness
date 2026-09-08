package original

import (
	"testing"

	// Make sure to replace below with the real import path if moved out of root.
	"mherrmann_gitignore_parser"
)

func TestAdvancedRuleParsing_SomeErrorBranches(t *testing.T) {
	rule := mherrmann_gitignore_parser.RuleFromPattern("/////")
	if rule == nil {
		t.Fatal("expected non-nil IgnoreRule for pattern '/////'")
	}
	if rule.Pattern != "/////" {
		t.Errorf("expected rule pattern to be '/////', got '%s'", rule.Pattern)
	}
}