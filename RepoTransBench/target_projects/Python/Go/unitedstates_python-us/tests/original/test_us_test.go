package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"unitedstates-go-us/us"
)

// test_attribute
func TestAttribute(t *testing.T) {
	for _, state := range us.StatesAndTerritories() {
		state2 := us.States.ByAbbr(state.Abbr)
		if !assert.Equal(t, state.Abbr, state2.Abbr) {
			t.Errorf("state abbr mismatch: %s vs %s", state.Abbr, state2.Abbr)
		}
		assert.Equal(t, state.FIPS, state2.FIPS)
		assert.Equal(t, state.Name, state2.Name)
		// Cover String() and GoString()
		assert.NotZero(t, state.String())
		assert.NotZero(t, state.GoString())
	}
}

// test_valid_timezones
func TestValidTimezones(t *testing.T) {
	for _, state := range us.StatesAndTerritories() {
		if state.Capital != "" {
			assert.True(t, us.ValidTimezone(state.CapitalTZ), "capital tz must be valid")
		}
		for _, tz := range state.TimeZones {
			assert.True(t, us.ValidTimezone(tz), "state timezone must be valid")
		}
		assert.Equal(t, len(state.TimeZones), len(uniqueStrings(state.TimeZones)), "no duplicate timezones")
	}
}
func uniqueStrings(ss []string) []string {
	keys := map[string]struct{}{}
	out := []string{}
	for _, v := range ss {
		if _, exists := keys[v]; !exists {
			keys[v] = struct{}{}
			out = append(out, v)
		}
	}
	return out
}

// test_fips
func TestFips(t *testing.T) {
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("24", "").Abbr)
	assert.NotEqual(t, us.States.MARYLAND.Abbr, us.Lookup("51", "").Abbr)
}

// test_abbr
func TestAbbr(t *testing.T) {
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("MD", "").Abbr)
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("md", "").Abbr)
	assert.NotEqual(t, us.States.MARYLAND.Abbr, us.Lookup("VA", "").Abbr)
	assert.NotEqual(t, us.States.MARYLAND.Abbr, us.Lookup("va", "").Abbr)
}

// test_name
func TestName(t *testing.T) {
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("Maryland", "").Abbr)
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("maryland", "").Abbr)
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("Maryland", "name").Abbr)
	assert.Nil(t, us.Lookup("maryland", "name"))
	assert.Equal(t, us.States.MARYLAND.Abbr, us.Lookup("murryland", "").Abbr)
	assert.NotEqual(t, us.States.MARYLAND.Abbr, us.Lookup("Virginia", "").Abbr)
}

// test_abbr_lookup
func TestAbbrLookup(t *testing.T) {
	for _, state := range us.States.List {
		found := us.Lookup(state.Abbr, "")
		assert.Equal(t, state.Abbr, found.Abbr)
		assert.Equal(t, state.Name, found.Name)
	}
}

// test_fips_lookup
func TestFipsLookup(t *testing.T) {
	for _, state := range us.States.List {
		found := us.Lookup(state.FIPS, "")
		assert.Equal(t, state.Abbr, found.Abbr)
		assert.Equal(t, state.Name, found.Name)
	}
}

// test_name_lookup
func TestNameLookup(t *testing.T) {
	for _, state := range us.States.List {
		found := us.Lookup(state.Name, "")
		assert.Equal(t, state.Abbr, found.Abbr)
		assert.Equal(t, state.Name, found.Name)
	}
}

// test_obsolete_lookup
func TestObsoleteLookup(t *testing.T) {
	for _, state := range us.Obsolete {
		assert.Nil(t, us.Lookup(state.Name, ""))
	}
}

// test_jellyfish_metaphone
func TestJellyfishMetaphone(t *testing.T) {
	for _, state := range append(us.StatesAndTerritories(), us.Obsolete...) {
		assert.Equal(t,
			us.Metaphone(state.Name), state.NameMetaphone,
			"metaphone must match")
	}
}

// test_mapping
func TestMapping(t *testing.T) {
	states := us.States.List[:5]
	expected := make(map[string]string)
	for _, s := range states {
		expected[s.Abbr] = s.FIPS
	}
	assert.Equal(t, expected, us.Mapping("abbr", "fips", states))
}

// test_obsolete_mapping
func TestObsoleteMapping(t *testing.T) {
	mapping := us.Mapping("abbr", "fips", nil)
	for _, state := range us.Obsolete {
		assert.NotContains(t, mapping, state.Abbr)
	}
}

// test_custom_mapping
func TestCustomMapping(t *testing.T) {
	mapping := us.Mapping("abbr", "fips", []us.State{us.States.DC, us.States.MARYLAND})
	assert.Equal(t, 2, len(mapping))
	assert.Contains(t, mapping, "DC")
	assert.Contains(t, mapping, "MD")
}

// test_kentucky_uppercase
func TestKentuckyUppercase(t *testing.T) {
	assert.Equal(t, us.States.KENTUCKY.Abbr, us.Lookup("kentucky", "").Abbr)
	assert.Equal(t, us.States.KENTUCKY.Abbr, us.Lookup("KENTUCKY", "").Abbr)
}

// test_wayoming
func TestWayoming(t *testing.T) {
	assert.Equal(t, us.States.WYOMING.Abbr, us.Lookup("Wyoming", "").Abbr)
	assert.Nil(t, us.Lookup("Wayoming", ""))
}

// test_dc
func TestDC(t *testing.T) {
	assert.NotContains(t, us.States.List, us.States.DC)
}

// test_obsolete
func TestObsolete(t *testing.T) {
	assert.Equal(t, 3, len(us.Obsolete))
}

// test_states
func TestStates(t *testing.T) {
	assert.Equal(t, 50, len(us.States.List))
}

// test_territories
func TestTerritories(t *testing.T) {
	assert.Equal(t, 5, len(us.Territories))
}

// test_contiguous
func TestContiguous(t *testing.T) {
	assert.Equal(t, 48, len(us.StatesContiguous))
}

// test_continental
func TestContinental(t *testing.T) {
	assert.Equal(t, 49, len(us.StatesContinental))
}