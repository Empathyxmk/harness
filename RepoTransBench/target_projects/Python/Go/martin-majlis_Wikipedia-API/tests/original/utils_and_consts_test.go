package original

import (
    "testing"
    "github.com/yourusername/wikipediaapi"
    "reflect"
    "strings"
)

func TestConstantsAreSet(t *testing.T) {
    if reflect.TypeOf(wikipediaapi.USER_AGENT).Kind() != reflect.String {
        t.Errorf("USER_AGENT type is not string")
    }
    if len(wikipediaapi.USER_AGENT) <= 10 {
        t.Errorf("USER_AGENT length too short: %d", len(wikipediaapi.USER_AGENT))
    }
    if reflect.TypeOf(wikipediaapi.MIN_USER_AGENT_LEN).Kind() != reflect.Int {
        t.Errorf("MIN_USER_AGENT_LEN type is not int")
    }
    if reflect.TypeOf(wikipediaapi.MAX_LANG_LEN).Kind() != reflect.Int {
        t.Errorf("MAX_LANG_LEN type is not int")
    }
}

func TestRESectionPatterns(t *testing.T) {
    wikiPat := wikipediaapi.RE_SECTION[wikipediaapi.ExtractFormatWIKI].Pattern
    htmlPat := wikipediaapi.RE_SECTION[wikipediaapi.ExtractFormatHTML].Pattern
    if !strings.HasPrefix(wikiPat, "\\n\\n") {
        t.Errorf("Expected wiki pattern prefix '\\n\\n', got %v", wikiPat)
    }
    if !strings.HasPrefix(htmlPat, "\\n? *<h([1-9])") {
        t.Errorf("Expected html pattern prefix '\\n? *<h([1-9])', got %v", htmlPat)
    }
}