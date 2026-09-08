package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Stand-in meta variables for __init__.py
var (
	environMetaVariables = map[string]interface{}{
		"copyright":      "Copyright (c) 2021-2024, Serghei Iakovlev",
		"version":        "1.0.0",
		"license":        "MIT",
		"author":         "Serghei Iakovlev",
		"author_email":   "oss@serghei.pl",
		"maintainer":     "Daniele Faraglia",
		"maintainer_email": "daniele.faraglia@gmail.com",
		"url":            "https://github.com/joke2k/django-environ",
		"description":    "Django-environ test package",
	}
)

func TestEnvironMetaVariables(t *testing.T) {
	for _, name := range []string{
		"copyright", "version", "license", "author", "author_email",
		"maintainer", "maintainer_email", "url", "description",
	} {
		_, ok := environMetaVariables[name]
		assert.True(t, ok)
	}
}

// Dummy functions for compatibility
func chooseRediscacheDriver(specPresent bool, djangoVer []int) string {
	if specPresent {
		return "django_redis.cache.RedisCache"
	}
	if len(djangoVer) >= 2 && djangoVer[0] >= 4 {
		return "django.core.cache.backends.redis.RedisCache"
	} else if len(djangoVer) >= 2 && djangoVer[0] < 4 {
		return "redis_cache.RedisCache"
	}
	return ""
}

func choosePostgresDriver(djangoVer []int) string {
	if len(djangoVer) >= 2 && djangoVer[0] == 1 && djangoVer[1] == 11 {
		return "django.db.backends.postgresql_psycopg2"
	} else if len(djangoVer) >= 2 && djangoVer[0] >= 3 {
		return "django.db.backends.postgresql"
	}
	return "django.db.backends.postgresql"
}

func choosePymemcacheDriver(djangoVer []int, hasSpec bool) string {
	if len(djangoVer) >= 2 && djangoVer[0] == 1 && djangoVer[1] == 11 {
		return "django.core.cache.backends.memcached.PyLibMCCache"
	}
	if len(djangoVer) >= 2 && djangoVer[0] >= 3 {
		if hasSpec {
			return "django.core.cache.backends.memcached.PyMemcacheCache"
		}
		return "django.core.cache.backends.memcached.PyLibMCCache"
	}
	return "django.core.cache.backends.memcached.PyLibMCCache"
}

func TestChooseRediscacheDriverPrecedence(t *testing.T) {
	v := chooseRediscacheDriver(true, []int{3, 2})
	assert.Equal(t, "django_redis.cache.RedisCache", v)
}

func TestChooseRediscacheDriverBuiltin(t *testing.T) {
	v := chooseRediscacheDriver(false, []int{4, 1})
	assert.Equal(t, "django.core.cache.backends.redis.RedisCache", v)
}

func TestChooseRediscacheDriverRedisCache(t *testing.T) {
	v := chooseRediscacheDriver(false, []int{3, 2})
	assert.Equal(t, "redis_cache.RedisCache", v)
}

func TestChoosePostgresDriver(t *testing.T) {
	assert.Equal(t, "django.db.backends.postgresql_psycopg2", choosePostgresDriver([]int{1, 11}))
	assert.Equal(t, "django.db.backends.postgresql", choosePostgresDriver([]int{3, 2}))
	assert.Equal(t, "django.db.backends.postgresql", choosePostgresDriver([]int{}))
}

func TestChoosePymemcacheDriver(t *testing.T) {
	assert.Equal(t, "django.core.cache.backends.memcached.PyLibMCCache", choosePymemcacheDriver([]int{1, 11}, false))
	assert.Equal(t, "django.core.cache.backends.memcached.PyLibMCCache", choosePymemcacheDriver([]int{3, 2}, false))
	assert.Equal(t, "django.core.cache.backends.memcached.PyMemcacheCache", choosePymemcacheDriver([]int{3, 2}, true))
	assert.Equal(t, "django.core.cache.backends.memcached.PyLibMCCache", choosePymemcacheDriver(nil, false))
}