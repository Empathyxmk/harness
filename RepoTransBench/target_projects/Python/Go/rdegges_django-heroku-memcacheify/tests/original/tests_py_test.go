package original

import (
	"os"
	"testing"

	. "github.com/stretchr/testify/assert"
	. "github.com/example/memcacheify"
)

func TestUsesLocalMemoryBackendIfNoMemcacheAddonIsAvailable(t *testing.T) {
	cleanup := clearEnvVars([]string{
		"MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
		"MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
		"MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
	})
	defer cleanup()
	expected := map[string]interface{}{"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
	Equal(t, memcacheify(), map[string]map[string]interface{}{"default": expected})
}

func TestUsesLocalMemoryBackendIfOneOfTheMemcacheEnvVarsIsMissing(t *testing.T) {
	cleanup := clearEnvVars([]string{
		"MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
	})
	defer cleanup()
	os.Setenv("MEMCACHE_PASSWORD", "GCnQ9DhfEJqNDlo1")
	os.Setenv("MEMCACHE_SERVERS", "mc3.ec2.northscale.net")
	expected := map[string]interface{}{"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
	Equal(t, memcacheify(), map[string]map[string]interface{}{"default": expected})
	os.Unsetenv("MEMCACHE_PASSWORD")
	os.Unsetenv("MEMCACHE_SERVERS")
}

func TestSetsProperBackendWhenMemcacheAddonIsAvailable(t *testing.T) {
	cleanup := clearEnvVars([]string{
		"MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
	})
	defer cleanup()
	os.Setenv("MEMCACHE_PASSWORD", "GCnQ9DhfEJqNDlo1")
	os.Setenv("MEMCACHE_SERVERS", "mc3.ec2.northscale.net")
	os.Setenv("MEMCACHE_USERNAME", "appxxxxx%40heroku.com")
	caches := memcacheify()
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
	os.Unsetenv("MEMCACHE_PASSWORD")
	os.Unsetenv("MEMCACHE_SERVERS")
	os.Unsetenv("MEMCACHE_USERNAME")
}

func TestUsesLocalMemoryBackendIfNoMemcachierAddonIsAvailable(t *testing.T) {
	cleanup := clearEnvVars([]string{
		"MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
	})
	defer cleanup()
	os.Setenv("MEMCACHIER_PASSWORD", "xxx")
	os.Setenv("MEMCACHIER_SERVERS", "mc1.ec2.memcachier.com")
	expected := map[string]interface{}{"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
	Equal(t, memcacheify(), map[string]map[string]interface{}{"default": expected})
	os.Unsetenv("MEMCACHIER_PASSWORD")
	os.Unsetenv("MEMCACHIER_SERVERS")
}

func TestSetsProperBackendWhenMemcachierAddonIsAvailable(t *testing.T) {
	cleanup := clearEnvVars([]string{
		"MEMCACHIER_PASSWORD", "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME",
		"MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
	})
	defer cleanup()
	os.Setenv("MEMCACHIER_PASSWORD", "xxx")
	os.Setenv("MEMCACHIER_SERVERS", "mc1.ec2.memcachier.com")
	os.Setenv("MEMCACHIER_USERNAME", "xxx")
	caches := memcacheify()
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
	Equal(t, os.Getenv("MEMCACHE_SERVERS"), os.Getenv("MEMCACHIER_SERVERS"))
	Equal(t, os.Getenv("MEMCACHE_USERNAME"), os.Getenv("MEMCACHIER_USERNAME"))
	Equal(t, os.Getenv("MEMCACHE_PASSWORD"), os.Getenv("MEMCACHIER_PASSWORD"))
	os.Unsetenv("MEMCACHIER_PASSWORD")
	os.Unsetenv("MEMCACHIER_SERVERS")
	os.Unsetenv("MEMCACHIER_USERNAME")
	os.Unsetenv("MEMCACHE_PASSWORD")
	os.Unsetenv("MEMCACHE_SERVERS")
	os.Unsetenv("MEMCACHE_USERNAME")
}

func TestSetsProperBackendWhenMemcachedcloudAddonIsAvailable(t *testing.T) {
	cleanup := clearEnvVars([]string{
		"MEMCACHEDCLOUD_PASSWORD", "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME",
		"MEMCACHE_PASSWORD", "MEMCACHE_SERVERS", "MEMCACHE_USERNAME",
	})
	defer cleanup()
	os.Setenv("MEMCACHEDCLOUD_PASSWORD", "xyz")
	os.Setenv("MEMCACHEDCLOUD_SERVERS", "zzzz")
	os.Setenv("MEMCACHEDCLOUD_USERNAME", "xyzzy")
	caches := memcacheify()
	Equal(t, "django_pylibmc.memcached.PyLibMCCache", caches["default"]["BACKEND"])
	Equal(t, os.Getenv("MEMCACHE_SERVERS"), os.Getenv("MEMCACHEDCLOUD_SERVERS"))
	Equal(t, os.Getenv("MEMCACHE_USERNAME"), os.Getenv("MEMCACHEDCLOUD_USERNAME"))
	Equal(t, os.Getenv("MEMCACHE_PASSWORD"), os.Getenv("MEMCACHEDCLOUD_PASSWORD"))
	os.Unsetenv("MEMCACHEDCLOUD_PASSWORD")
	os.Unsetenv("MEMCACHEDCLOUD_SERVERS")
	os.Unsetenv("MEMCACHEDCLOUD_USERNAME")
	os.Unsetenv("MEMCACHE_PASSWORD")
	os.Unsetenv("MEMCACHE_SERVERS")
	os.Unsetenv("MEMCACHE_USERNAME")
}

// helper from testutil, in this package for simplicity
func clearEnvVars(keys []string) func() {
	originals := make(map[string]string)
	for _, k := range keys {
		if v, found := os.LookupEnv(k); found {
			originals[k] = v
			os.Unsetenv(k)
		}
	}
	return func() {
		for _, k := range keys {
			os.Unsetenv(k)
		}
		for k, v := range originals {
			os.Setenv(k, v)
		}
	}
}