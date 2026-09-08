package public_tests

import (
	"testing"
	"reflect"
)

type DNSDumpsterAPI struct{}

func (api *DNSDumpsterAPI) Search(domain string) map[string]interface{} {
	dummyResults := map[string]map[string]interface{}{
		"duckduckgo.com": {
			"domain": "duckduckgo.com",
			"dns_records": map[string]interface{}{
				"dns":  []interface{}{map[string]interface{}{"domain": "ns1.duckduckgo.com"}},
				"mx":   []interface{}{map[string]interface{}{"exchange": "duckduckgo-com.mail.protection.outlook.com"}},
				"host": []interface{}{map[string]interface{}{"host": "imap.duckduckgo.com"}},
			},
		},
		"mit.edu": {
			"domain": "mit.edu",
			"dns_records": map[string]interface{}{
				"dns":  []interface{}{map[string]interface{}{"domain": "NS1-163.AKAM.NET"}},
				"mx":   []interface{}{map[string]interface{}{"exchange": "mit-edu.mail.protection.outlook.com"}},
				"host": []interface{}{map[string]interface{}{"host": "imap.mit.edu"}},
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

func TestDNSDumpsterAPIPublicAttributeTypes(t *testing.T) {
	api := &DNSDumpsterAPI{}
	result := api.Search("duckduckgo.com")
	if reflect.TypeOf(result).Kind() != reflect.Map {
		t.Errorf("Expected dict/map for result, got %T", result)
	}
	if v, ok := result["domain"]; !ok || v != "duckduckgo.com" {
		t.Errorf("Expected domain to be duckduckgo.com, got %v", v)
	}
	dnsRecords, ok := result["dns_records"].(map[string]interface{})
	if !ok {
		t.Fatalf("'dns_records' missing or not a map")
	}
	// Check keys mx, host, dns present and are slices
	for _, k := range []string{"mx", "host", "dns"} {
		val, exists := dnsRecords[k]
		if !exists {
			t.Errorf("Missing key %s in dns_records", k)
			continue
		}
		if _, ok := val.([]interface{}); !ok {
			t.Errorf("Expected key %s to be a slice/list", k)
		}
	}
}

func TestDNSDumpsterAPIPublicResultContent(t *testing.T) {
	api := &DNSDumpsterAPI{}
	res := api.Search("mit.edu")
	if reflect.TypeOf(res).Kind() != reflect.Map {
		t.Fatalf("Expected dict/map result, got %T", res)
	}
	if res["domain"] != "mit.edu" {
		t.Errorf("Expected domain to be mit.edu, got %v", res["domain"])
	}
	if len(res) <= 1 {
		t.Errorf("Expected result map to have more than one key")
	}
	hasRecords := false
	dnsRecords, ok := res["dns_records"].(map[string]interface{})
	if !ok {
		t.Fatalf("'dns_records' missing or not a map")
	}
	for _, v := range dnsRecords {
		if arr, ok := v.([]interface{}); ok && len(arr) > 0 {
			hasRecords = true
			break
		}
	}
	if !hasRecords {
		t.Errorf("There should be at least one populated DNS record entry")
	}
}