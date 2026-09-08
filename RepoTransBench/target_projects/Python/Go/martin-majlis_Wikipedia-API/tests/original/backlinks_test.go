package original

import (
	"sort"
	"testing"
	"github.com/yourusername/wikipediaapi"
	// Assume testutil contains mocks/mocking helpers
)

func TestBacklinksNonexistentCount(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Non_Existent")
	backlinks := page.Backlinks()
	if len(backlinks) != 0 {
		t.Errorf("Expected 0 backlinks for non-existent page, got %d", len(backlinks))
	}
}

func TestBacklinksSinglePageCount(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Test_1")
	backlinks := page.Backlinks()
	if len(backlinks) != 3 {
		t.Errorf("Expected 3 backlinks, got %d", len(backlinks))
	}
}

func TestBacklinksSinglePageTitles(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Test_1")
	backlinks := page.Backlinks()
	var got []string
	for _, v := range backlinks {
		got = append(got, v.Title)
	}
	sort.Strings(got)
	var exp []string
	for i := 0; i < 3; i++ {
		exp = append(exp, "Title - "+testutil.Str(i+1))
	}
	testutil.AssertStringSliceEqual(t, got, exp)
}

func TestBacklinksMultiPageCount(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Test_2")
	backlinks := page.Backlinks()
	if len(backlinks) != 5 {
		t.Errorf("Expected 5 backlinks, got %d", len(backlinks))
	}
}

func TestBacklinksMultiPageTitles(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Test_2")
	backlinks := page.Backlinks()
	var got []string
	for _, v := range backlinks {
		got = append(got, v.Title)
	}
	sort.Strings(got)
	var exp []string
	for i := 0; i < 5; i++ {
		exp = append(exp, "Title - "+testutil.Str(i+1))
	}
	testutil.AssertStringSliceEqual(t, got, exp)
}