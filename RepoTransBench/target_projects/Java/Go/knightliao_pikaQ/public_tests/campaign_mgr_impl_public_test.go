package public_tests

import (
	"testing"
)

type CampaignMgrImpl struct{}

func TestCampaignMgrImplInstanceNotNull(t *testing.T) {
	mgr := &CampaignMgrImpl{}
	if mgr == nil {
		t.Error("CampaignMgrImpl instantiation failed")
	}
}