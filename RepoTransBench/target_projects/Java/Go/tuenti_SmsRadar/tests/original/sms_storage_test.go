package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type DummySmsStorage struct {
	last  int
	first bool
}

func (d *DummySmsStorage) UpdateLastSmsIntercepted(id int) {
	d.last = id
	d.first = false
}
func (d *DummySmsStorage) GetLastSmsIntercepted() int { return d.last }
func (d *DummySmsStorage) IsFirstSmsIntercepted() bool { return d.first }
func (d *DummySmsStorage) AddSms(s Sms)                {}
func (d *DummySmsStorage) GetAllSms() []Sms            { return nil }
func (d *DummySmsStorage) Clear()                      {}

func TestSmsStorage_IsFirstSmsInterceptedInitiallyTrue(t *testing.T) {
	storage := &DummySmsStorage{last: -1, first: true}
	assert.True(t, storage.IsFirstSmsIntercepted())
}

func TestSmsStorage_UpdateAndGetLastSms(t *testing.T) {
	storage := &DummySmsStorage{last: -1, first: true}
	storage.UpdateLastSmsIntercepted(42)
	assert.False(t, storage.IsFirstSmsIntercepted())
	assert.Equal(t, 42, storage.GetLastSmsIntercepted())
}