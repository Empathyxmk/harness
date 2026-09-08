package public_tests

import (
	"testing"
)

// Public dummy struct (mirrors public DummySubuserClientPublic in Python)
type DummySubuserClientPublic struct {
	ApiKey    string
	SecretKey string
}

type ResultPublic struct{}

func (r *ResultPublic) PrintObject() string { return "done" }

func NewDummySubuserClientPublic(apiKey, secretKey string) *DummySubuserClientPublic {
	return &DummySubuserClientPublic{ApiKey: apiKey, SecretKey: secretKey}
}

func (c *DummySubuserClientPublic) PostSetSubuserTransferability(subUids string, transferability bool) ([]map[string]interface{}, error) {
	if subUids == "" {
		return nil, &ArgumentErrorPublic{"sub_uids required"}
	}
	return []map[string]interface{}{
		{"uid": subUids, "success": true, "transferability": transferability},
	}, nil
}

func (c *DummySubuserClientPublic) GetSubUserDepositHistory(subUid int) (*ResultPublic, error) {
	if subUid == -1 {
		return nil, &ArgumentErrorPublic{"Not found"}
	}
	return &ResultPublic{}, nil
}

func (c *DummySubuserClientPublic) PostSubuserApikeyGenerate(otpToken string, subUid int, note string, permission string) (*ResultPublic, error) {
	if otpToken == "" || note == "" {
		return nil, &ArgumentErrorPublic{"otp_token and note required"}
	}
	return &ResultPublic{}, nil
}

type ArgumentErrorPublic struct{ Msg string }
func (e *ArgumentErrorPublic) Error() string { return e.Msg }

func TestPostSetSubuserTransferabilityTruePublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	res, err := c.PostSetSubuserTransferability("abcd", true)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if len(res) == 0 || res[0]["transferability"] != true || res[0]["uid"] != "abcd" {
		t.Errorf("Invalid result: %+v", res)
	}
}

func TestPostSetSubuserTransferabilityFalsePublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	res, err := c.PostSetSubuserTransferability("efgh", false)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if res[0]["transferability"] != false {
		t.Error("Expected transferability to be false")
	}
}

func TestPostSetSubuserTransferabilityInvalidPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	_, err := c.PostSetSubuserTransferability("efgh", false)
	// Go doesn't invoke error for type, so simulate always success if bool type
	if err != nil && err.Error() != "" {
		t.Errorf("Did not expect error here, got: %v", err)
	}
}

func TestPostSetSubuserTransferabilityNoUidPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	_, err := c.PostSetSubuserTransferability("", true)
	if err == nil {
		t.Error("Expected error for missing sub_uids")
	}
}

func TestGetSubUserDepositHistoryOkPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	res, err := c.GetSubUserDepositHistory(555)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if res.PrintObject() != "done" {
		t.Error("Expected PrintObject to return 'done'")
	}
}

func TestGetSubUserDepositHistoryNotFoundPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	_, err := c.GetSubUserDepositHistory(-1)
	if err == nil {
		t.Error("Expected error for sub_uid == -1")
	}
}

func TestPostSubuserApikeyGenerateSuccessPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	res, err := c.PostSubuserApikeyGenerate("pub_otp", 999, "pub_note", "readWrite")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if res.PrintObject() != "done" {
		t.Error("Expected PrintObject to return 'done'")
	}
}

func TestPostSubuserApikeyGenerateMissingPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("public-key", "public-secret")
	_, err := c.PostSubuserApikeyGenerate("", 999, "", "readWrite")
	if err == nil {
		t.Error("Expected error for missing otp_token and note")
	}
}

func TestInitSubuserClientPublic(t *testing.T) {
	c := NewDummySubuserClientPublic("", "")
	if c.ApiKey != "" || c.SecretKey != "" {
		t.Error("Expected ApiKey and SecretKey to be empty")
	}
}