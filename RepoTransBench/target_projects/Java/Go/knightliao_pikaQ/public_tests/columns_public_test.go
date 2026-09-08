package public_tests

import "testing"

const (
	NAME       = "name"
	CAMPAIGN_ID = "campaignId"
)

func TestNameConstantNotNull(t *testing.T) {
	if NAME == "" {
		t.Error("NAME should not be empty or nil")
	}
	if len(NAME) <= 2 {
		t.Errorf("NAME should have length > 2, got %v", len(NAME))
	}
}

func TestCampaignIdConstantHasId(t *testing.T) {
	l := len(CAMPAIGN_ID)
	if l < 2 || CAMPAIGN_ID[l-2:] != "Id" {
		t.Errorf("CAMPAIGN_ID %q does not end with Id", CAMPAIGN_ID)
	}
}