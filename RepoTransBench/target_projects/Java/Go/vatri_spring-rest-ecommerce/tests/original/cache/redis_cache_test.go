package cache

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

func TestRedisCache_GetList(t *testing.T) {
    cache := testsutil.NewRedisCache()
    cache.Sets["item"] = map[string]struct{}{
        "{id:1}": {},
        "{id:2}": {},
    }
    list := cache.GetList("item", testsutil.MockObj{})
    for _, o := range list {
        require.NotNil(t, o)
        assert.GreaterOrEqual(t, o.ID, 1, "ID not set")
    }
}

func TestRedisCache_GetItem(t *testing.T) {
    cache := testsutil.NewRedisCache()
    cache.Data["item"] = "{id:1}"
    o := cache.GetItem("item", testsutil.MockObj{})
    require.NotNil(t, o)
    assert.Greater(t, o.ID, 0)
}

func TestRedisCache_AddObjectToList(t *testing.T) {
    cache := testsutil.NewRedisCache()
    out := cache.AddItemToList("item", testsutil.MockObj{ID: 1})
    assert.Equal(t, 2, len(out))
}

func TestRedisCache_RemoveObjectFromList(t *testing.T) {
    cache := testsutil.NewRedisCache()
    cache.AddItemToList("item", testsutil.MockObj{ID: 1})
    out := cache.RemoveItemFromList("item", testsutil.MockObj{ID: 1})
    assert.Equal(t, 1, len(out))
}

func TestRedisCache_AddingObjectToCache(t *testing.T) {
    cache := testsutil.NewRedisCache()
    res := cache.SetItem("new_item", testsutil.MockObj{ID: 1})
    assert.Equal(t, 1, res.ID)
}