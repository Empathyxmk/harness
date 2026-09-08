package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type GmailSyncer struct {
	Initialized bool
	LastSync    []string
}

func (g *GmailSyncer) Init() {
	g.Initialized = true
}

func (g *GmailSyncer) Sync(msgs []string) {
	g.LastSync = msgs
}

func TestGmailSyncer_DifferentInitTriggersSyncPublic(t *testing.T) {
	syncer := &GmailSyncer{}
	syncer.Init()
	assert.True(t, syncer.Initialized)
	msgs := []string{}
	syncer.Sync(msgs)
	assert.Equal(t, msgs, syncer.LastSync)
}