package docx

import (
	"testing"
)

func TestCanReadDocumentWithSingleParagraphWithSingleRunOfText(t *testing.T) {
	t.Skip("Requires Go docx.read and document model implementation")
}

func TestMainDocumentIsFoundUsingPackageRelationships(t *testing.T) {
	t.Skip("Requires Go docx.read and document relationships implementation")
}

func TestErrorIsRaisedWhenMainDocumentPartDoesNotExist(t *testing.T) {
	t.Skip("Requires Go docx.read and document relationships implementation")
}

func TestMainDocumentPartIsFoundUsingPackageRelationships(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestWhenRelationshipForMainDocumentCannotBeFoundThenFallbackIsUsed(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestCommentsPartIsFoundUsingMainDocumentRelationships(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestWhenRelationshipForCommentsCannotBeFoundThenFallbackIsUsed(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestEndnotesPartIsFoundUsingMainDocumentRelationships(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestWhenRelationshipForEndnotesCannotBeFoundThenFallbackIsUsed(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestFootnotesPartIsFoundUsingMainDocumentRelationships(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestWhenRelationshipForFootnotesCannotBeFoundThenFallbackIsUsed(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestNumberingPartIsFoundUsingMainDocumentRelationships(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestWhenRelationshipForNumberingCannotBeFoundThenFallbackIsUsed(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestStylesPartIsFoundUsingMainDocumentRelationships(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}

func TestWhenRelationshipForStylesCannotBeFoundThenFallbackIsUsed(t *testing.T) {
	t.Skip("Requires Go docx.PartPaths logic")
}