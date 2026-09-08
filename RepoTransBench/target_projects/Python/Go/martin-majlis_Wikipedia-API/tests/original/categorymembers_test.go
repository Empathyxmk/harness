package original

import (
	"sort"
	"testing"
	"github.com/yourusername/wikipediaapi"
)

func TestCategoryMembers_SinglePageCount(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Category:C1")
	cats := page.CategoryMembers()
	if len(cats) != 3 {
		t.Errorf("Expected 3 category members, got %d", len(cats))
	}
}

func TestCategoryMembers_SinglePageTitles(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Category:C1")
	cats := page.CategoryMembers()
	var got []string
	for _, v := range cats {
		got = append(got, v.Title)
	}
	sort.Strings(got)
	var exp []string
	for i := 0; i < 3; i++ {
		exp = append(exp, "Title - "+testutil.Str(i+1))
	}
	testutil.AssertStringSliceEqual(t, got, exp)
}

func TestCategoryMembers_MultiPageCount(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Category:C2")
	cats := page.CategoryMembers()
	if len(cats) != 5 {
		t.Errorf("Expected 5 category members, got %d", len(cats))
	}
}

func TestCategoryMembers_MultiPageTitles(t *testing.T) {
	wiki := testutil.NewMockWikipedia("en")
	page := wiki.Page("Category:C2")
	cats := page.CategoryMembers()
	var got []string
	for _, v := range cats {
		got = append(got, v.Title)
	}
	sort.Strings(got)
	var exp []string
	for i := 0; i < 5; i++ {
		exp = append(exp, "Title - "+testutil.Str(i+1))
	}
	testutil.AssertStringSliceEqual(t, got, exp)
}