package original

import (
	"os"
	"testing"
	. "github.com/stretchr/testify/assert"
)

import (
	. "github.com/example/memcacheify"
)

func cleanEnviron(t *testing.T) func() {
	relevant := []string{
		"MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
		"MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
		"MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
		"MEMCACHEIFY_USE_LOCAL",
	}
	originals := make(map[string]string)
	for _, k := range relevant {
		if v, found := os.LookupEnv(k); found {
			originals[k] = v
			os.Unsetenv(k)
		}
	}
	return func() {
		for _, k := range relevant {
			os.Unsetenv(k)
		}
		for k, v := range originals {
			os.Setenv(k, v)
		}
	}
}

func TestLocalCacheDefault(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	caches := memcacheify()
	Equal(t, "django.core.cache.backends.locmem.LocMemCache", caches["default"]["BACKEND"])
}

func TestMemcacheEnvVarsMissing(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	os.Setenv("MEMCACHE_PASSWORD", "pass")
	os.Setenv("MEMCACHE_SERVERS", "host")
	caches := memcacheify()
	Equal(t, "django.core.cache.backends.locmem.LocMemCache", caches["default"]["BACKEND"])
}

func TestMemcacheEnvVarsSet(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	os.Setenv("MEMCACHE_PASSWORD", "pass")
	os.Setenv("MEMCACHE_SERVERS", "host")
	os.Setenv("MEMCACHE_USERNAME", "user")
	caches := memcacheify(map[string]interface{}{"TIMEOUT": 111})
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
	Equal(t, "localhost:11211", caches["default"]["LOCATION"])
	Equal(t, 111, caches["default"]["TIMEOUT"])
}

func TestMemcachierEnvVarsSet(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	os.Setenv("MEMCACHIER_PASSWORD", "pw")
	os.Setenv("MEMCACHIER_SERVERS", "host1,host2")
	os.Setenv("MEMCACHIER_USERNAME", "user")
	caches := memcacheify(map[string]interface{}{"TIMEOUT": 123})
	loc := caches["default"]["LOCATION"].(string)
	Expect := []string{"host1;host2", "host1,host2"}
	Contains(t, Expect, loc)
	Equal(t, 123, caches["default"]["TIMEOUT"])
	Equal(t, os.Getenv("MEMCACHE_SERVERS"), "host1;host2")
	Equal(t, os.Getenv("MEMCACHE_USERNAME"), "user")
	Equal(t, os.Getenv("MEMCACHE_PASSWORD"), "pw")
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
}

func TestMemcachedcloudEnvVarsSet(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	os.Setenv("MEMCACHEDCLOUD_PASSWORD", "pwcloud")
	os.Setenv("MEMCACHEDCLOUD_SERVERS", "c1,c2")
	os.Setenv("MEMCACHEDCLOUD_USERNAME", "clouduser")
	caches := memcacheify(map[string]interface{}{"TIMEOUT": 321})
	loc := caches["default"]["LOCATION"].(string)
	Expect := []string{"c1;c2", "c1,c2"}
	Contains(t, Expect, loc)
	Equal(t, 321, caches["default"]["TIMEOUT"])
	Equal(t, os.Getenv("MEMCACHE_SERVERS"), "c1;c2")
	Equal(t, os.Getenv("MEMCACHE_USERNAME"), "clouduser")
	Equal(t, os.Getenv("MEMCACHE_PASSWORD"), "pwcloud")
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
}

func TestMemcacheifyUseLocal(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	os.Setenv("MEMCACHEIFY_USE_LOCAL", "1")
	caches := memcacheify()
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
}

func TestMemcachierIncomplete(t *testing.T) {
	combinations := [][]string{
		{"MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS"},
		{"MEMCACHIER_PASSWORD"},
	}
	for _, missing := range combinations {
		reset := cleanEnviron(t)
		os.Setenv("MEMCACHIER_PASSWORD", "pw")
		os.Setenv("MEMCACHIER_SERVERS", "h1")
		os.Setenv("MEMCACHIER_USERNAME", "u1")
		for _, m := range missing {
			os.Unsetenv(m)
		}
		caches := memcacheify()
		Equal(t, "django.core.cache.backends.locmem.LocMemCache", caches["default"]["BACKEND"])
		reset()
	}
}

func TestMemcachedcloudIncomplete(t *testing.T) {
	combinations := [][]string{
		{"MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS"},
		{"MEMCACHEDCLOUD_PASSWORD"},
	}
	for _, missing := range combinations {
		reset := cleanEnviron(t)
		os.Setenv("MEMCACHEDCLOUD_PASSWORD", "pw")
		os.Setenv("MEMCACHEDCLOUD_SERVERS", "h1")
		os.Setenv("MEMCACHEDCLOUD_USERNAME", "u1")
		for _, m := range missing {
			os.Unsetenv(m)
		}
		caches := memcacheify()
		Equal(t, "django.core.cache.backends.locmem.LocMemCache", caches["default"]["BACKEND"])
		reset()
	}
}

func TestMemcacheifyTimeoutDefault(t *testing.T) {
	reset := cleanEnviron(t)
	defer reset()
	os.Setenv("MEMCACHE_PASSWORD", "p")
	os.Setenv("MEMCACHE_SERVERS", "h")
	os.Setenv("MEMCACHE_USERNAME", "u")
	caches := memcacheify()
	Equal(t, 500, caches["default"]["TIMEOUT"])
}