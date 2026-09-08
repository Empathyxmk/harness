package html

import (
	"testing"
)

func TestCollapsingDoesNothingToSingleTextNode(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestConsecutiveFreshElementsAreNotCollapsed(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestConsecutiveCollapsibleElementsAreCollapsedIfTheyHaveTheSameTagAndAttributes(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestElementsWithDifferentTagNamesAreNotCollapsed(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestElementsWithDifferentAttributesAreNotCollapsed(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestChildrenOfCollapsedElementCanCollapseWithChildrenOfPreviousElement(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestCollapsibleElementCanCollapseIntoPreviousFreshElement(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestElementWithChoiceOfTagNamesCanCollapseIntoPreviousElementIfItHasOneOfThoseTagNamesAsItsMainTagName(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}

func TestWhenSeparatorIsPresentThenSeparatorIsPrependedToCollapsedElement(t *testing.T) {
	t.Skip("Requires Go html.collapse implementation")
}