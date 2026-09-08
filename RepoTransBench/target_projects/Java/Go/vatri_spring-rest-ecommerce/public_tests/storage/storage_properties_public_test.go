package storage

import (
    "testing"
    "github.com/stretchr/testify/assert"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

func TestDefaultLocationPublic(t *testing.T) {
    p := testsutil.NewStorageProperties()
    assert.NotEqual(t, "somewhereelse", p.GetLocation())
    assert.Equal(t, "uploads", p.GetLocation())
}

func TestSetLocationPublic(t *testing.T) {
    p := testsutil.NewStorageProperties()
    p.SetLocation("my_new_location")
    assert.Equal(t, "my_new_location", p.GetLocation())
    assert.NotEqual(t, "abc", p.GetLocation())
}