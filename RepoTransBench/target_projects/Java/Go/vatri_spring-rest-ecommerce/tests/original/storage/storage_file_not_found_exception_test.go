package storage

import (
    "errors"
    "testing"
    "github.com/stretchr/testify/assert"
    testsutil "github.com/example/vatri_spring_rest_ecommerce/tests"
)

func TestMessageConstructor(t *testing.T) {
    ex := testsutil.NewStorageFileNotFoundException("testmsg", nil)
    assert.Equal(t, "testmsg", ex.Error())
}

func TestMessageAndCauseConstructor(t *testing.T) {
    cause := errors.New("inner")
    ex := testsutil.NewStorageFileNotFoundException("outer", cause)
    assert.Equal(t, "outer", ex.Error())
    assert.Equal(t, cause, ex.Unwrap())
}