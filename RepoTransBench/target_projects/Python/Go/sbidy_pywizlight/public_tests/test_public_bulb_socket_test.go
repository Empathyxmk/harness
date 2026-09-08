package public_tests

import (
	"testing"
)

type SocketFeatures struct {
	Color bool
}
type TestBulb struct {
	BulbName   string
	FeatureSet SocketFeatures
}
func getSocketBulbTypes() map[string]TestBulb {
	return map[string]TestBulb{
		"ESP32_SOCKET": {BulbName: "Wiz ESP32 Power Socket", FeatureSet: SocketFeatures{Color: false}},
	}
}

func TestBulbTypePublic(t *testing.T) {
	types := getSocketBulbTypes()

	if _, ok := types["ESP32_SOCKET"]; !ok {
		t.Error("ESP32_SOCKET should exist")
	}
	s := types["ESP32_SOCKET"]
	if s.BulbName != "Wiz ESP32 Power Socket" {
		t.Errorf("ESP32_SOCKET BulbName = %v", s.BulbName)
	}
	if s.FeatureSet.Color != false {
		t.Error("ESP32_SOCKET Color feature should be false")
	}

	if _, ok := types["SOCKET_XYZ"]; ok {
		t.Error("SOCKET_XYZ should not exist")
	}
}