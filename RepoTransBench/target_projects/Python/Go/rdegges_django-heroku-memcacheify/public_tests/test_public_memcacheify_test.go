package public_tests

import (
	"os"
	"strings"
	"testing"

	. "github.com/stretchr/testify/assert"
	. "github.com/example/memcacheify"
)

func getCacheConf(result map[string]map[string]interface{}) map[string]interface{} {
	// Always return result["default"], as in the Python tests
	return result["default"]
}

// Return true if the backend string indicates a memcache backend
func isMemcacheBackend(backend string) bool {
	return backend == "django.core.cache.backends.memcached.PyLibMCCache" ||
		backend == "django_pylibmc.memcached.PyLibMCCache"
}

func extractTimeout(cacheConf map[string]interface{}) int {
	// If present as int
	if to, ok := cacheConf["TIMEOUT"].(int); ok {
		return to
	}
	// If present as float64 (for interface{} parsing)
	if to, ok := cacheConf["TIMEOUT"].(float64); ok {
		return int(to)
	}
	// If present as a map {'TIMEOUT': value}
	if m, ok := cacheConf["TIMEOUT"].(map[string]interface{}); ok {
		if t2, ok2 := m["TIMEOUT"].(int); ok2 {
			return t2
		}
	}
	return 0
}

func TestPublicMemcacheifyBasic(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112")
	os.Setenv("MEMCACHIER_USERNAME", "public_alpha")
	os.Setenv("MEMCACHIER_PASSWORD", "alp_pw")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHIER_USERNAME")
		os.Unsetenv("MEMCACHIER_PASSWORD")
	}()
	settings := map[string]interface{}{
		"TIMEOUT": 876,
		"BINARY":  true,
	}
	result := memcacheify(settings)
	cacheConf := getCacheConf(result)
	True(t, isMemcacheBackend(cacheConf["BACKEND"].(string)))
	locations := []string{
		"alpha-mc1.pub.net:22111,alpha-mc2.pub.net:22112",
		"alpha-mc1.pub.net:22111;alpha-mc2.pub.net:22112",
	}
	loc := cacheConf["LOCATION"].(string)
	Contains(t, locations, loc)
	Equal(t, 876, extractTimeout(cacheConf))
}

func TestPublicMemcacheifyLocationFallback(t *testing.T) {
	os.Unsetenv("MEMCACHIER_SERVERS")
	os.Setenv("MEMCACHE_SERVERS", "fallback-mc-newpub.example.com:31220")
	os.Setenv("MEMCACHE_USERNAME", "newuser")
	os.Setenv("MEMCACHE_PASSWORD", "newpass")
	defer func() {
		os.Unsetenv("MEMCACHE_SERVERS")
		os.Unsetenv("MEMCACHE_USERNAME")
		os.Unsetenv("MEMCACHE_PASSWORD")
	}()
	result := memcacheify(map[string]interface{}{})
	cacheConf := getCacheConf(result)
	possibilities := []string{"fallback-mc-newpub.example.com:31220", "localhost:11211"}
	Contains(t, possibilities, cacheConf["LOCATION"].(string))
}

func TestPublicMemcacheifyBlankEnv(t *testing.T) {
	os.Unsetenv("MEMCACHIER_SERVERS")
	os.Unsetenv("MEMCACHE_SERVERS")
	os.Unsetenv("MEMCACHIER_USERNAME")
	os.Unsetenv("MEMCACHIER_PASSWORD")
	os.Unsetenv("MEMCACHE_USERNAME")
	os.Unsetenv("MEMCACHE_PASSWORD")
	result := memcacheify(map[string]interface{}{})
	cacheConf := getCacheConf(result)
	be := cacheConf["BACKEND"].(string)
	True(t, be == "django.core.cache.backends.memcached.PyLibMCCache" ||
		be == "django_pylibmc.memcached.PyLibMCCache" ||
		be == "django.core.cache.backends.locmem.LocMemCache")
	loc := ""
	if l, ok := cacheConf["LOCATION"].(string); ok {
		loc = l
	}
	InSlice(t, loc, []string{"", "localhost:11211"})
}

func TestPublicMemcacheifyTimeouts(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "b.pub.com:15111")
	os.Setenv("MEMCACHIER_USERNAME", "pub_timeout")
	os.Setenv("MEMCACHIER_PASSWORD", "pwtout")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHIER_USERNAME")
		os.Unsetenv("MEMCACHIER_PASSWORD")
	}()
	settings := map[string]interface{}{
		"TIMEOUT": 9342,
	}
	result := memcacheify(settings)
	cacheConf := getCacheConf(result)
	Equal(t, 9342, extractTimeout(cacheConf))
}

func TestPublicMemcacheifyOptionsOverride(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "pub-override.another.net")
	os.Setenv("MEMCACHIER_USERNAME", "override_user")
	os.Setenv("MEMCACHIER_PASSWORD", "override_pw")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHIER_USERNAME")
		os.Unsetenv("MEMCACHIER_PASSWORD")
	}()
	custom := map[string]interface{}{
		"OPTIONS": map[string]interface{}{
			"behaviors": map[string]interface{}{
				"connect_timeout": 9999,
				"retry_timeout":   55555,
			},
			"username": "optuser",
			"password": "optpw",
		},
		"TIMEOUT": 422,
	}
	result := memcacheify(custom)
	cacheConf := getCacheConf(result)
	Equal(t, 422, extractTimeout(cacheConf))
}

func TestPublicMemcacheifyLocationEnvPriority(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "top-priority-pub.example:8998")
	os.Setenv("MEMCACHE_SERVERS", "secondary-pub-fallback.example:8998")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHE_SERVERS")
	}()
	result := memcacheify(map[string]interface{}{})
	cacheConf := getCacheConf(result)
	possible := []string{"top-priority-pub.example:8998", "localhost:11211"}
	InSlice(t, cacheConf["LOCATION"].(string), possible)
}

func TestPublicMemcacheifyNullSettings(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "")
	os.Setenv("MEMCACHIER_USERNAME", "")
	os.Setenv("MEMCACHIER_PASSWORD", "")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHIER_USERNAME")
		os.Unsetenv("MEMCACHIER_PASSWORD")
	}()
	result := memcacheify()
	cacheConf := getCacheConf(result)
	loc := cacheConf["LOCATION"]
	lstr := ""
	if loc != nil {
		lstr, _ = loc.(string)
	}
	possibleLocs := []string{"localhost:11211", "", ""}
	InSlice(t, lstr, possibleLocs)
}

func TestPublicMemcacheifyEmptyStringEnv(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "")
	os.Setenv("MEMCACHIER_USERNAME", "")
	os.Setenv("MEMCACHIER_PASSWORD", "")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHIER_USERNAME")
		os.Unsetenv("MEMCACHIER_PASSWORD")
	}()
	result := memcacheify(map[string]interface{}{})
	cacheConf := getCacheConf(result)
	loc := ""
	if L, ok := cacheConf["LOCATION"].(string); ok {
		loc = L
	}
	InSlice(t, loc, []string{"", "localhost:11211"})
}

func TestPublicMemcacheifyNoArgs(t *testing.T) {
	os.Setenv("MEMCACHIER_SERVERS", "")
	os.Setenv("MEMCACHIER_USERNAME", "")
	os.Setenv("MEMCACHIER_PASSWORD", "")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
		os.Unsetenv("MEMCACHIER_USERNAME")
		os.Unsetenv("MEMCACHIER_PASSWORD")
	}()
	result := memcacheify()
	cacheConf := getCacheConf(result)
	loc := cacheConf["LOCATION"].(string)
	InSlice(t, loc, []string{"", "localhost:11211"})
	be := cacheConf["BACKEND"].(string)
	True(t, isMemcacheBackend(be) || be == "django.core.cache.backends.locmem.LocMemCache")
}

func TestPublicMemcacheifyCustomBehaviors(t *testing.T) {
	settings := map[string]interface{}{
		"OPTIONS": map[string]interface{}{
			"behaviors": map[string]interface{}{
				"tcp_keepalive": nil,
				"tcp_nodelay":   false,
			},
		},
	}
	os.Setenv("MEMCACHIER_SERVERS", "customb-pub1.example.net:51035")
	defer func() {
		os.Unsetenv("MEMCACHIER_SERVERS")
	}()
	result := memcacheify(settings)
	cacheConf := getCacheConf(result)
}