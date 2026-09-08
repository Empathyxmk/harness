package storage

import (
    "testing"
    "github.com/stretchr/testify/assert"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

func TestDefaultLocation(t *testing.T) {
    p := testsutil.NewStorageProperties()
    assert.Equal(t, "uploads", p.GetLocation())
}

func TestSetLocation(t *testing.T) {
    p := testsutil.NewStorageProperties()
    p.SetLocation("abc")
    assert.Equal(t, "abc", p.GetLocation())
}