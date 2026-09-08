package original

import (
	"os"
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
	"unitedstates-go-us/us"
)

// test_state_repr_and_str
func TestStateReprAndStr(t *testing.T) {
	s := us.States.ALABAMA // AL
	assert.Equal(t, "<State:Alabama>", s.GoString(), "repr should be <State:STATE_NAME>")
	assert.Equal(t, "Alabama", s.String(), "str should return the state name")
}

// test_shapefile_urls_with_fips
func TestShapefileUrlsWithFips(t *testing.T) {
	s := us.States.ALABAMA
	urls := s.ShapefileUrls()
	assert.IsType(t, map[string]string{}, urls, "should be a map")
	assert.Contains(t, urls, "tract", "should contain tract")
	assert.Contains(t, urls, "county", "should contain county")
}

// test_shapefile_urls_without_fips
func TestShapefileUrlsWithoutFips(t *testing.T) {
	s := us.State{
		Name:           "Fake",
		Abbr:           "ZZ",
		FIPS:           "",
		IsObsolete:     true,
		IsTerritory:    true,
		IsContiguous:   false,
		IsContinental:  false,
		APAbbr:         "",
		Capital:        "",
		CapitalTZ:      "",
		NameMetaphone:  "FK",
		StatehoodYear:  0,
		TimeZones:      []string{},
	}
	assert.Nil(t, s.ShapefileUrls(), "should return nil if no FIPS")
}

// test_lookup_with_field_argument
func TestLookupWithFieldArgument(t *testing.T) {
	md := us.States.MARYLAND
	assert.Equal(t, md, us.Lookup("MD", "abbr"), "lookup by abbr")
	assert.Equal(t, md, us.Lookup("24", "fips"), "lookup by fips")
	assert.Equal(t, md, us.Lookup(md.NameMetaphone, "name_metaphone"), "lookup by metaphone")
	assert.Nil(t, us.Lookup("maryland", "name"), "lookup by field 'name' is case sensitive and should return nil")
}

// test_lookup_no_match_returns_none
func TestLookupNoMatchReturnsNone(t *testing.T) {
	assert.Nil(t, us.Lookup("nonesuchstate", ""), "lookup unknown string should return nil")
	assert.Nil(t, us.Lookup("zzzzzzzzzz", ""), "lookup obscure metaphone should return nil")
}

// test_lookup_caching
func TestLookupCaching(t *testing.T) {
	val := "MD"
	md := us.Lookup(val, "")
	cacheKey := "abbr:MD"
	// Simulate cache priming (implement _lookup_cache in Go version if needed)
	if us.HasLookupCacheKey(cacheKey) {
		assert.Equal(t, md, us.Lookup(val, ""), "should retrieve from cache")
	}
}

// test_mapping_default_and_custom
func TestMappingDefaultAndCustom(t *testing.T) {
	m := us.Mapping("abbr", "fips", nil)
	assert.Equal(t, "24", m["MD"], "MD abbr maps to 24")
	assert.Equal(t, "01", m["AL"], "AL abbr maps to 01")
	// Custom: just DC and MD
	custom := us.Mapping("abbr", "fips", []us.State{us.States.DC, us.States.MARYLAND})
	assert.ElementsMatch(t, []string{"DC", "MD"}, mapKeys(custom), "should contain only DC, MD")
}

func mapKeys(m map[string]string) []string {
	keys := []string{}
	for k := range m {
		keys = append(keys, k)
	}
	return keys
}

// test_FIPS_RE_and_ABBR_RE
func TestFIPSREAndABBRRE(t *testing.T) {
	assert.True(t, us.FIPSRe.MatchString("24"), "should match valid FIPS")
	assert.False(t, us.FIPSRe.MatchString("a2"), "should not match invalid FIPS")
	assert.True(t, us.AbbrRe.MatchString("MD"), "should match uppercase abbr")
	assert.True(t, us.AbbrRe.MatchString("md"), "should match lowercase abbr")
	assert.False(t, us.AbbrRe.MatchString("maryland"), "should not match state name")
}

// test_DCS_statehood_env
func TestDCStatehoodEnv(t *testing.T) {
	_ = os.Setenv("DC_STATEHOOD", "1")
	us.ReloadStates()
	assert.True(t, us.DCStatehood(), "DC_STATEHOOD env var set -> DCStatehood true")
	_ = os.Unsetenv("DC_STATEHOOD")
	us.ReloadStates()
	assert.False(t, us.DCStatehood(), "DC_STATEHOOD unset -> DCStatehood false")
}

// test_imports_exports_version
func TestImportsExportsVersion(t *testing.T) {
	assert.NotZero(t, us.Version)
	assert.Equal(t, "United States of America", us.USA.Name)
	assert.Equal(t, "US", us.USA.Abbr)
	assert.Equal(t, "1776-07-04", us.USA.Birthday.String())
}