package tests

import (
	"testing"
)

func TestPlainParagraphIsConvertedToPlainParagraph(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestMultipleParagraphsAreConvertedToMultipleParagraphs(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestEmptyParagraphsAreIgnored(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestStyleMappingsUsingStyleIdsCanBeUsedToMapParagraphs(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestStyleMappingsUsingStyleNamesCanBeUsedToMapParagraphs(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestStyleNamesInStyleMappingsAreCaseInsensitive(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDefaultParagraphStyleIsUsedIfNoMatchingStyleIsFound(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDefaultParagraphStyleIsSpecifiedByMappingPlainParagraphs(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestWarningIsEmittedIfParagraphStyleIsUnrecognised(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestNoWarningIfThereIsNoStyleForPlainParagraphs(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBulletedParagraphsAreConvertedUsingMatchingStyles(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBulletedStylesDontMatchPlainParagraph(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBoldRunsAreWrappedInStrongTagsByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBoldRunsCanBeConfiguredWithStyleMapping(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestItalicRunsAreWrappedInEmphasisTagsByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestItalicRunsCanBeConfiguredWithStyleMapping(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestUnderlineRunsAreIgnoredByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestUnderlineRunsCanBeMappedUsingStyleMapping(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestStyleMappingForUnderlineRunsDoesNotCloseParentElements(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestStrikethroughRunsAreWrappedInSElementsByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestStrikethroughRunsCanBeConfiguredWithStyleMapping(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestAllCapsRunsAreIgnoredByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestAllCapsRunsCanBeMappedUsingStyleMapping(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestSmallCapsRunsAreIgnoredByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestSmallCapsRunsCanBeMappedUsingStyleMapping(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestHighlightedRunsAreIgnoredByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestHighlightedRunsCanBeConfiguredWithStyleMappingForAllHighlights(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestHighlightedRunsCanBeConfiguredWithStyleMappingForSpecificHighlightColor(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestSuperscriptRunsAreWrappedInSupTags(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestSubscriptRunsAreWrappedInSubTags(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestRunsAreConvertedBySatisfyingMatchingPaths(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDocxHyperlinkWithHrefIsConvertedToAnchorTag(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDocxHyperlinksCanBeCollapsed(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDocxHyperlinkWithInternalAnchorReferenceIsConvertedToAnchorTag(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestHyperlinkTargetFrameIsUsedAsAnchorTarget(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestUncheckedCheckboxIsConvertedToUncheckedCheckboxInput(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestCheckedCheckboxIsConvertedToCheckedCheckboxInput(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBookmarksAreConvertedToAnchorsWithIds(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDocxTabIsConvertedToTabInHtml(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestDocxTableIsConvertedToTableInHtml(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestTableStyleMappingsCanBeUsedToMapTables(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestHeaderRowsAreWrappedInThead(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestTbodyIsOmittedIfAllRowsAreHeaders(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestUnexpectedTableChildrenDoNotCauseError(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestEmptyCellsArePreservedInTable(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestEmptyRowsArePreservedInTable(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestTableCellsAreWrittenWithColspanIfNotEqualToOne(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestTableCellsAreWrittenWithRowspanIfNotEqualToOne(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestLineBreakIsConvertedToBr(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBreaksThatAreNotLineBreaksAreIgnored(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestBreaksCanBeMappedUsingStyleMappings(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestImagesAreConvertedToImgTagsWithDataUri(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestImagesHaveAltTagsIfAvailable(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestCanDefineCustomConversionForImages(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestFootnoteReferenceIsConvertedToSuperscriptIntraPageLink(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestFootnotesAreIncludedAfterTheMainBody(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestCommentsAreIgnoredByDefault(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestCommentReferencesAreLinkedToCommentAfterMainBody(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestWhenInitialsAreNotBlankThenCommentAuthorLabelIsInitials(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}

func TestWhenInitialsAreBlankThenCommentAuthorLabelIsBlank(t *testing.T) {
	t.Skip("Requires Go mammoth.conversion implementation")
}