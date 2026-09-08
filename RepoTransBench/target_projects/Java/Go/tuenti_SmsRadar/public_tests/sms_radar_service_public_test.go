package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsRadarServicePublic_Stub(t *testing.T) {
	service := &SmsRadarService{}
	assert.NotNil(t, service)
}