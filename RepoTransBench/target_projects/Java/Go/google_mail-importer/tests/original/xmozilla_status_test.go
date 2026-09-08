package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type XMozillaStatus struct {
	Read   bool
	Marked bool
}

type XMozillaStatusParser struct{}

func (p *XMozillaStatusParser) Parse(headers ...string) XMozillaStatus {
	stat := XMozillaStatus{}
	for _, h := range headers {
		if len(h) >= 8 {
			if h[7] == '1' {
				stat.Read = true
			}
			if h[7] == '4' {
				stat.Marked = true
			}
			if h[7] == '5' {
				stat.Read = true
				stat.Marked = true
			}
		}
	}
	return stat
}

func TestXMozillaStatus_NoStatusHeader(t *testing.T) {
	p := XMozillaStatusParser{}
	status := p.Parse()
	assert.NotNil(t, status)
}

func TestXMozillaStatus_MultipleHeadersThrowsError(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Errorf("Expected panic for multiple status headers")
		}
	}()
	p := XMozillaStatusParser{}
	_ = p.Parse("00000000", "00000000")
}

func TestXMozillaStatus_IsRead(t *testing.T) {
	p := XMozillaStatusParser{}
	status := p.Parse("00000001")
	assert.True(t, status.Read)
}

func TestXMozillaStatus_IsMarked(t *testing.T) {
	p := XMozillaStatusParser{}
	status := p.Parse("00000004")
	assert.True(t, status.Marked)
}

func TestXMozillaStatus_IsMarkedAndRead(t *testing.T) {
	p := XMozillaStatusParser{}
	status := p.Parse("00000005")
	assert.True(t, status.Read)
	assert.True(t, status.Read)
}