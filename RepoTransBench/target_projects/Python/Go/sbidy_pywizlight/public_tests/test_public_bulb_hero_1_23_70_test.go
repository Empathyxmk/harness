package public_tests

import (
	"testing"
)

type BulbFeature struct {
	Color bool
}
type BulbType struct {
	Features BulbFeature
	BulbName string
}
func getBulbTypes() map[string]BulbType {
	return map[string]BulbType{
		"ESP01_SHDW_12WW": {Features: BulbFeature{Color: false}, BulbName: "ESP01_SHDW_12WW"},
	}
}

func TestBulbHero12370Public(t *testing.T) {
	bulbTypes := getBulbTypes()
	if _, ok := bulbTypes["HERO_PUBLIC"]; ok {
		t.Error("HERO_PUBLIC should not exist in bulbTypes")
	}
	tt, ok := bulbTypes["ESP01_SHDW_12WW"]
	if !ok {
		t.Fatal("ESP01_SHDW_12WW should exist")
	}
	if tt.Features.Color != false {
		t.Error("Expected color feature false for ESP01_SHDW_12WW")
	}
}