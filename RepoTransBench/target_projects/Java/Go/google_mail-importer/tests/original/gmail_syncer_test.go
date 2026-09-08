package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

type Mailbox interface {
	Init() error
	MapMessageIDs([]string) map[string][]string
	UploadMessage(msg interface{}) error
}

type GmailSyncer struct {
	Mailbox    Mailbox
	Initialized bool
}

func NewGmailSyncer(mailbox Mailbox) *GmailSyncer {
	return &GmailSyncer{Mailbox: mailbox}
}

func (gs *GmailSyncer) Init() error {
	gs.Initialized = true
	return nil
}

func (gs *GmailSyncer) Sync(messages []string) error {
	if !gs.Initialized {
		return errors.New("init not called")
	}
	for _, msg := range messages {
		// Simulate upload
		_ = gs.Mailbox.UploadMessage(msg)
	}
	return nil
}

type fakeMailbox struct {
	Called   bool
	Uploads  []string
}

func (fm *fakeMailbox) Init() error {
	fm.Called = true
	return nil
}

func (fm *fakeMailbox) MapMessageIDs(msgs []string) map[string][]string {
	return make(map[string][]string)
}

func (fm *fakeMailbox) UploadMessage(msg interface{}) error {
	fm.Uploads = append(fm.Uploads, msg.(string))
	return nil
}

func TestGmailSyncer_InitRequiredBeforeSync(t *testing.T) {
	mailbox := &fakeMailbox{}
	syncer := NewGmailSyncer(mailbox)
	err := syncer.Sync([]string{})
	assert.Error(t, err, "sync() should fail if init() is not called first.")
}

func TestGmailSyncer_SyncEmptyList(t *testing.T) {
	mailbox := &fakeMailbox{}
	syncer := NewGmailSyncer(mailbox)
	require.NoError(t, syncer.Init())
	err := syncer.Sync([]string{})
	assert.NoError(t, err)
	assert.Equal(t, 0, len(mailbox.Uploads))
}

func TestGmailSyncer_SyncWithMessages(t *testing.T) {
	mailbox := &fakeMailbox{}
	syncer := NewGmailSyncer(mailbox)
	require.NoError(t, syncer.Init())
	err := syncer.Sync([]string{"Subject 1", "Subject 2"})
	assert.NoError(t, err)
	assert.Equal(t, []string{"Subject 1", "Subject 2"}, mailbox.Uploads)
}