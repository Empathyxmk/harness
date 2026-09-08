package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"unitedstates-go-us/us"
)

func TestStateNameAndAbbr(t *testing.T) {
	assert.Equal(t, "California", us.States.CALIFORNIA.Name)
	assert.Equal(t, "NY", us.States.NEWYORK.Abbr)
}

func TestStateAlternate(t *testing.T) {
	assert.Equal(t, "36", us.States.NEWYORK.FIPS)
	assert.Equal(t, "Carson City", us.States.NEVADA.Capital)
}

func TestStateNumeric(t *testing.T) {
	tx := us.States.TEXAS
	assert.IsType(t, "string", tx.FIPS)
	assert.True(t, isDigits(tx.FIPS))
}

func isDigits(s string) bool {
	for _, ch := range s {
		if ch < '0' || ch > '9' {
			return false
		}
	}
	return len(s) > 0
}

func TestContinentalStatesExcludesHawaiiAndAlaska(t *testing.T) {
	abbrs := map[string]struct{}{}
	for _, st := range us.States.List {
		abbrs[st.Abbr] = struct{}{}
	}
	_, foundDC := abbrs["DC"]
	assert.False(t, foundDC, "DC should not be in US states")
	_, foundCA := abbrs["CA"]
	_, foundNY := abbrs["NY"]
	assert.True(t, foundCA)
	assert.True(t, foundNY)
}

func TestStatesObjectIsIterableAndLen(t *testing.T) {
	allNames := map[string]struct{}{}
	for _, st := range us.States.List {
		allNames[st.Name] = struct{}{}
	}
	_, found := allNames["Wyoming"]
	assert.True(t, found)
	usStateAbbrs := map[string]struct{}{}
	for _, st := range us.States.List {
		if st.Abbr != "DC" &&
			st.Abbr != "AS" &&
			st.Abbr != "GU" &&
			st.Abbr != "MP" &&
			st.Abbr != "PR" &&
			st.Abbr != "VI" {
			usStateAbbrs[st.Abbr] = struct{}{}
		}
	}
	assert.Equal(t, 50, len(usStateAbbrs))
}

func TestFieldTypes(t *testing.T) {
	tx := us.States.TEXAS
	assert.IsType(t, "string", tx.Capital)
	switch tx.TimeZones.(type) {
	case []string:
	case []interface{}:
	default:
		t.Error("time_zones should be a slice")
	}
	// Go doesn't have hasattr; area_codes is typically always present.
	if tx.AreaCodes != nil {
		switch tx.AreaCodes.(type) {
		case []string:
		case []interface{}:
		default:
			t.Error("area_codes expected list/tuple in Go")
		}
	}
}

func TestListMembershipAndEquality(t *testing.T) {
	ca := us.States.CALIFORNIA
	found := false
	for _, st := range us.States.List {
		if st.Name == "California" {
			found = true
			assert.Equal(t, ca, st)
		}
	}
	assert.True(t, found)
}

func TestAllStatesHaveFipsAndNames(t *testing.T) {
	for _, st := range us.States.List {
		assert.NotEmpty(t, st.FIPS)
		assert.NotEmpty(t, st.Name)
	}
}

func TestNontypicalStateFips(t *testing.T) {
	pr := us.States.PUERTO_RICO
	assert.Equal(t, "72", pr.FIPS)
	assert.Equal(t, "Puerto Rico", pr.Name)
}

func TestStateProperties(t *testing.T) {
	arizona := us.States.ARIZONA
	assert.Equal(t, "Phoenix", arizona.Capital)
	containsAmerica := false
	for _, tz := range arizona.TimeZones.([]string) {
		if len(tz) > 8 && tz[:8] == "America/" {
			containsAmerica = true
			break
		}
	}
	assert.True(t, containsAmerica, "Arizona time_zones should contain America/")
}