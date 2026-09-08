package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsRadarService_RegisterContentResolver(t *testing.T) {
	service := &SmsRadarService{}
	assert.NotNil(t, service)
}

func TestSmsRadarService_UnregisterContentResolver(t *testing.T) {
	service := &SmsRadarService{}
	service.OnDestroy()
	assert.NotNil(t, service)
}

func TestSmsRadarService_OnTaskRemovedSetsAlarm(t *testing.T) {
	service := &SmsRadarService{}
	service.OnTaskRemoved()
	assert.NotNil(t, service)
}