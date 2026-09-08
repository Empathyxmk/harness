package handlers

import (
	"testing"
)

func TestGCPHandlerEmitsProperly(t *testing.T) {
	gcpEvent := map[string]interface{}{
		"protoPayload": map[string]interface{}{
			"methodName": "storage.objects.insert",
			"resourceName": "projects/_/buckets/mybucket/objects/myobj",
		},
	}
	got, err := HandleGCP(gcpEvent)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := "Handled GCP event: method=storage.objects.insert resource=projects/_/buckets/mybucket/objects/myobj"
	if got != want {
		t.Errorf("HandleGCP response mismatch. got: %v, want: %v", got, want)
	}
}

func HandleGCP(evt map[string]interface{}) (string, error) {
	payload := evt["protoPayload"].(map[string]interface{})
	method := payload["methodName"].(string)
	resource := payload["resourceName"].(string)
	return "Handled GCP event: method=" + method + " resource=" + resource, nil
}