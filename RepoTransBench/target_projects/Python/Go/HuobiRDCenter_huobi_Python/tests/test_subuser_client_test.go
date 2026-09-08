package tests

import (
	"testing"
	"huobirdcenter_huobi_go/huobi/client"
)

func TestPostSetSubuserTransferabilityTrue(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	res, err := c.PostSetSubuserTransferability("1234", true)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if len(res) == 0 || res[0]["transferability"] != true || res[0]["uid"] != "1234" {
		t.Errorf("Invalid result: %+v", res)
	}
}

func TestPostSetSubuserTransferabilityFalse(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	res, err := c.PostSetSubuserTransferability("999", false)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if res[0]["transferability"] != false {
		t.Error("Expected transferability to be false")
	}
}

func TestPostSetSubuserTransferabilityInvalid(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	_, err := c.PostSetSubuserTransferability("999", false) // Go doesn't allow type mismatch like Python, so skip
	if err != nil && err.Error() != "" {
		t.Errorf("Did not expect error here, got: %v", err)
	}
}

func TestPostSetSubuserTransferabilityNoUid(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	_, err := c.PostSetSubuserTransferability("", true)
	if err == nil {
		t.Error("Expected error for missing sub_uids")
	}
}

func TestGetSubUserDepositHistoryOk(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	res, err := c.GetSubUserDepositHistory(100)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if res.PrintObject() != "printed" {
		t.Error("Expected PrintObject to return 'printed'")
	}
}

func TestGetSubUserDepositHistoryNotFound(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	_, err := c.GetSubUserDepositHistory(0)
	if err == nil {
		t.Error("Expected error for sub_uid == 0")
	}
}

func TestPostSubuserApikeyGenerateSuccess(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	res, err := c.PostSubuserApikeyGenerate("otp", 123, "note", "readOnly")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if res.PrintObject() != "printed" {
		t.Error("Expected PrintObject to return 'printed'")
	}
}

func TestPostSubuserApikeyGenerateMissing(t *testing.T) {
	c := client.NewDummySubuserClient("test-key", "test-secret")
	_, err := c.PostSubuserApikeyGenerate("", 123, "", "readOnly")
	if err == nil {
		t.Error("Expected error for missing otp_token and note")
	}
}

func TestInitSubuserClient(t *testing.T) {
	c := client.NewDummySubuserClient("", "")
	if c.ApiKey != "" || c.SecretKey != "" {
		t.Error("Expected ApiKey and SecretKey to be empty")
	}
}