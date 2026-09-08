package writers

import (
	"testing"
)

func TestSpecialMarkdownCharactersAreEscaped(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestUnrecognisedElementsAreTreatedAsNormalText(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestParagraphsAreTerminatedWithDoubleNewLine(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestH1ElementsAreConvertedToHeadingWithLeadingHash(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestH6ElementsAreConvertedToHeadingWithSixLeadingHashes(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestBrIsWrittenAsTwoSpacesFollowedByNewline(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestStrongTextIsSurroundedByTwoUnderscores(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestEmphasisedTextIsSurroundedByOneAsterix(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestAnchorTagsAreWrittenAsHyperlinks(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestAnchorTagsWithoutHrefAttributeAreTreatedAsOrdinaryText(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestElementsWithIdsHaveAnchorTagsWithIdsAppendedToStartOfMarkdownElement(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestLinksHaveAnchorsBeforeOpeningSquareBracket(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestImageElementsAreWrittenAsMarkdownImages(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestImagesAreWrittenEvenIfTheyDontHaveAltText(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestImagesAreWrittenEvenIfTheyDontHaveASrcAttribute(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestImageElementsAreIgnoredIfTheyHaveNoSrcAndNoAltText(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestListItemOutsideOfListIsTreatedAsUnorderedList(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestOlElementIsWrittenAsOrderedListWithSequentialNumbering(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestUlElementIsWrittenAsUnorderedListUsingHyphensAsBullets(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}

func TestNumberingIsSeparateForNestedListAndParentList(t *testing.T) {
	t.Skip("Requires Go MarkdownWriter implementation")
}