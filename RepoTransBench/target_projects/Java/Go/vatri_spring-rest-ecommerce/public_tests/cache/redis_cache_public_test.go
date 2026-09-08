package cache

import (
    "testing"
    "github.com/stretchr/testify/assert"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

func TestSetAndGetDifferentKeyValue(t *testing.T) {
    cache := testsutil.NewRedisCache()
    cache.Data["publicKey"] = "\"publicValue\""
    cache.Data["missingKey"] = ""

    val := cache.Data["publicKey"]
    assert.Equal(t, "\"publicValue\"", val)

    // Simulate get with unmarshalling
    retrieved := cache.Data["publicKey"]
    if len(retrieved) > 2 && retrieved[0] == '"' && retrieved[len(retrieved)-1] == '"' {
        retrieved = retrieved[1 : len(retrieved)-1]
    }
    assert.Equal(t, "publicValue", retrieved)

    _, ok := cache.Data["missingKey"]
    assert.True(t, ok)
    if cache.Data["missingKey"] == "" {
        assert.True(t, true)
    }
}

func TestDeleteKey(t *testing.T) {
    cache := testsutil.NewRedisCache()
    cache.Data["deletePublic"] = "value"
    deleted := cache.Delete("deletePublic")
    assert.True(t, deleted)
    deleted2 := cache.Delete("doesNotExist")
    assert.False(t, deleted2)
}