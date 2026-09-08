package public_tests

import (
	"testing"
	"reflect"
)

//--- DummyResponse and DNSDumpsterAPI Mocks

type DNSDumpsterAPI struct{}

func (api *DNSDumpsterAPI) Search(domain string) map[string]interface{} {
	dummyResults := map[string]map[string]interface{}{
		"openai.com": {
			"domain": "openai.com",
			"dns_records": map[string]interface{}{
				"dns":  []interface{}{map[string]interface{}{"domain": "ns1.openai.com"}},
				"mx":   []interface{}{map[string]interface{}{"exchange": "aspmx.l.google.com"}},
				"host": []interface{}{map[string]interface{}{"host": "mail.openai.com"}},
			},
		},
		"duckduckgo.com": {
			"domain": "duckduckgo.com",
			"dns_records": map[string]interface{}{
				"dns":  []interface{}{map[string]interface{}{"domain": "ns1.duckduckgo.com"}},
				"mx":   []interface{}{map[string]interface{}{"exchange": "duckduckgo-com.mail.protection.outlook.com"}},
				"host": []interface{}{map[string]interface{}{"host": "imap.duckduckgo.com"}},
			},
		},
	}

	if v, ok := dummyResults[domain]; ok {
		return v
	}
	return map[string]interface{}{
		"domain": domain,
		"dns_records": map[string]interface{}{
			"dns":  []interface{}{},
			"mx":   []interface{}{},
			"host": []interface{}{},
		},
	}
}

func TestDNSDumpsterAPIPublicSearch(t *testing.T) {
	api := &DNSDumpsterAPI{}
	result := api.Search("openai.com")
	if reflect.TypeOf(result).Kind() != reflect.Map {
		t.Fatalf("Expected dict/map result, got %T", result)
	}
	if result["domain"] != "openai.com" {
		t.Errorf("Expected 'domain' to be openai.com, got %v", result["domain"])
	}
	dnsRecords, ok := result["dns_records"].(map[string]interface{})
	if !ok {
		t.Fatalf("'dns_records' missing or not a map")
	}
	nonEmpty := false
	for _, key := range []string{"dns", "mx", "host"} {
		val := dnsRecords[key]
		if arr, isArr := val.([]interface{}); isArr && len(arr) > 0 {
			nonEmpty = true
			break
		}
	}
	if !nonEmpty {
		t.Errorf("At least one DNS record list should not be empty")
	}
}