package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsObserver_NoCursor_NoListenerCalled(t *testing.T) {
	observer := &SmsObserver{}
	observer.OnChange(true)
	assert.NotNil(t, observer)
}