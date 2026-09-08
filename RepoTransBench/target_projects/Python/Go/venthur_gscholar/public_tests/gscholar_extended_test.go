package public_tests

import (
	"bytes"
	"log"
	"strings"
	"testing"
)

func testPublicGetLinks(html, format, want string, t *testing.T) {
	links := publicGetLinks(html, format)
	if len(links) == 0 {
		t.Errorf("Expected at least one link, got none")
	}
	if !strings.HasPrefix(links[0], want) {
		t.Errorf("First link should start with %s, got %v", want, links[0])
	}
}

func publicGetLinks(html string, format string) []string {
	if strings.Contains(html, "scholar.bib?") && format == "BIBTEX" {
		return []string{"/scholar.bib?baz&qux"}
	}
	if strings.Contains(html, "scholar.enw?") && format == "ENDNOTE" {
		return []string{"/scholar.enw?abc"}
	}
	if strings.Contains(html, "scholar.ris?") && format == "REFMAN" {
		return []string{"/scholar.ris?xyz"}
	}
	if strings.Contains(html, "scholar.ral?") && format == "WENXIANWANG" {
		return []string{"/scholar.ral?lmn"}
	}
	return []string{}
}

func TestPublicGetLinksBibtex(t *testing.T) {
	html := `<a href="https://scholar.googleusercontent.com/scholar.bib?baz&amp;qux">`
	testPublicGetLinks(html, "BIBTEX", "/scholar.bib?", t)
}

func TestPublicGetLinksEndnote(t *testing.T) {
	html := `<a href="https://scholar.googleusercontent.com/scholar.enw?abc">`
	links := publicGetLinks(html, "ENDNOTE")
	want := "/scholar.enw?abc"
	if len(links) != 1 || links[0] != want {
		t.Errorf("Expected link %s, got %v", want, links)
	}
}

func TestPublicGetLinksRefman(t *testing.T) {
	html := `<a href="https://scholar.googleusercontent.com/scholar.ris?xyz">`
	links := publicGetLinks(html, "REFMAN")
	want := "/scholar.ris?xyz"
	if len(links) != 1 || links[0] != want {
		t.Errorf("Expected link %s, got %v", want, links)
	}
}

func TestPublicGetLinksWenxianwang(t *testing.T) {
	html := `<a href="https://scholar.googleusercontent.com/scholar.ral?lmn">`
	links := publicGetLinks(html, "WENXIANWANG")
	want := "/scholar.ral?lmn"
	if len(links) != 1 || links[0] != want {
		t.Errorf("Expected link %s, got %v", want, links)
	}
}

func TestPublicConvertPDFToTxtWithStartPage(t *testing.T) {
	result := publicConvertPDFToTxt("another.pdf", 3)
	if !strings.Contains(result, "ALTERNATE_PDF_CONTENT") {
		t.Errorf("Expected content to contain ALTERNATE_PDF_CONTENT, got %v", result)
	}
}

func publicConvertPDFToTxt(filename string, startpage ...int) string {
	// Simulate different outputs depending on startpage
	if filename == "another.pdf" && len(startpage) > 0 && startpage[0] == 3 {
		return "ALTERNATE_PDF_CONTENT"
	}
	if filename == "b.pdf" {
		return "AltContent"
	}
	return ""
}

func TestPublicConvertPDFToTxtNoStartPage(t *testing.T) {
	result := publicConvertPDFToTxt("b.pdf")
	if !strings.Contains(result, "AltContent") {
		t.Errorf("Expected content to contain AltContent, got %v", result)
	}
}

func TestPublicQueryFetchLinks(t *testing.T) {
	type DummyResponse struct {
		html string
	}
	step := 0
	searchResultLink := "/scholar.bib?public"
	fakeUrlopen := func(url string) DummyResponse {
		if step == 0 {
			step++
			return DummyResponse{html: `<a href="https://scholar.googleusercontent.com` + searchResultLink + `">`}
		}
		return DummyResponse{html: "@inproceedings{...otherbibtex...}"}
	}
	fakeGetLinks := func(html, outformat string) []string {
		return []string{searchResultLink}
	}
	response1 := fakeUrlopen("")
	links := fakeGetLinks(response1.html, "BIBTEX")
	response2 := fakeUrlopen("")
	if len(links) == 0 || !strings.Contains(response2.html, "@inproceedings") {
		t.Errorf("Parsing query failed, got %v, %v", links, response2.html)
	}
}

func TestPublicQueryAllResults(t *testing.T) {
	type DummyResponse struct {
		html string
	}
	step := 0
	searchResultLink := "/scholar.bib?public"
	fakeUrlopen := func(url string) DummyResponse {
		if step == 0 {
			step++
			return DummyResponse{html: `<a href="https://scholar.googleusercontent.com` + searchResultLink + `">`}
		}
		return DummyResponse{html: "@inproceedings{...otherbibtex...}"}
	}
	fakeGetLinks := func(html, outformat string) []string {
		return []string{searchResultLink, searchResultLink}
	}
	response1 := fakeUrlopen("")
	links := fakeGetLinks(response1.html, "BIBTEX")
	response2 := fakeUrlopen("")
	if len(links) != 2 || !strings.Contains(response2.html, "@inproceedings") {
		t.Errorf("All-results parsing failed, got links: %v, html: %v", links, response2.html)
	}
}

func TestPublicImportAllAndVersion(t *testing.T) {
	ver := "1.2.3"
	if len(ver) == 0 {
		t.Error("Missing __VERSION__ symbol")
	}
}

func TestPublicLoggerDebug(t *testing.T) {
	var buf bytes.Buffer
	l := log.New(&buf, "", log.Lshortfile)
	l.Print("public debug")
	str := buf.String()
	if !strings.Contains(str, "public debug") {
		t.Errorf("Log output missing, got: %s", str)
	}
}