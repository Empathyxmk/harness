package storage

import (
    "errors"
    "testing"
    "github.com/stretchr/testify/assert"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

func TestMessageConstructorPublic(t *testing.T) {
    ex := testsutil.NewStorageFileNotFoundException("public-message", nil)
    assert.Equal(t, "public-message", ex.Error())
}

func TestMessageAndCauseConstructorPublic(t *testing.T) {
    cause := errors.New("different-inner")
    ex := testsutil.NewStorageFileNotFoundException("different-outer", cause)
    assert.Equal(t, "different-outer", ex.Error())
    assert.Equal(t, cause, ex.Unwrap())
}