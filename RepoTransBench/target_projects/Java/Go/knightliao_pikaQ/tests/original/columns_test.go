package original

import "testing"

const (
	NAME       = "name"
	CAMPAIGN_ID = "campaignId"
)

func TestNameConstant(t *testing.T) {
	if NAME != "name" {
		t.Errorf("NAME = %s, expected name", NAME)
	}
}

func TestCampaignIdConstant(t *testing.T) {
	if CAMPAIGN_ID != "campaignId" {
		t.Errorf("CAMPAIGN_ID = %s, expected campaignId", CAMPAIGN_ID)
	}
}