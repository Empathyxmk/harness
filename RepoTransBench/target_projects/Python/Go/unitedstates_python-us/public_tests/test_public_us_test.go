package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"unitedstates-go-us/us"
)

func TestFipsLookup(t *testing.T) {
	assert.Equal(t, us.States.TEXAS, us.Lookup("48", ""), "lookup by FIPS 48 -> TX")
}

func TestAbbrLookup(t *testing.T) {
	assert.Equal(t, us.States.COLORADO, us.Lookup("CO", ""), "lookup by abbr CO -> CO")
}

func TestNameLookup(t *testing.T) {
	assert.Equal(t, us.States.FLORIDA, us.Lookup("Florida", ""), "lookup by name Florida")
}

func TestMetaphoneLookup(t *testing.T) {
	assert.Equal(t, us.States.MINNESOTA, us.Lookup("Minissota", ""), "metaphone fuzzy lookup")
}

func TestMetaphoneLookupCaps(t *testing.T) {
	assert.Equal(t, us.States.ILLINOIS, us.Lookup("ILLINOYS", ""), "metaphone fuzzy lookup (caps)")
}

func TestLookupWithIntegerInput(t *testing.T) {
	assert.Equal(t, us.States.FLORIDA, us.Lookup("12", ""), "lookup by fips string '12'")
}

func TestLookupWithField(t *testing.T) {
	assert.Equal(t, us.States.WISCONSIN, us.Lookup("Madison", "capital"), "lookup by field capital=Madison")
}

func TestNonexistantLookupReturnsNone(t *testing.T) {
	assert.Nil(t, us.Lookup("GOTHAMCITY", ""), "lookup should return nil for bogus value")
}

func TestTerritoryLookup(t *testing.T) {
	assert.Equal(t, us.States.PUERTO_RICO, us.Lookup("PR", ""), "lookup should find PR")
}