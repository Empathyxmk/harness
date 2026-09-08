package public_tests

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
)

type PrintStreamCommandOutput struct {
	out *bytes.Buffer
}

func (p *PrintStreamCommandOutput) Print(s string) {
	p.out.WriteString(s)
}
func (p *PrintStreamCommandOutput) Println(s string) {
	p.out.WriteString(s + "\n")
}
func (p *PrintStreamCommandOutput) Flush() {}

func TestOutputPrintsMessage(t *testing.T) {
	out := new(bytes.Buffer)
	po := &PrintStreamCommandOutput{out: out}
	testMessage := "PublicTestLine 42"
	po.Print(testMessage)
	po.Flush()
	result := out.String()
	assert.Contains(t, result, testMessage)
}

func TestOutputPrintsAnotherMessage(t *testing.T) {
	out := new(bytes.Buffer)
	po := &PrintStreamCommandOutput{out: out}
	testMessage := "AnotherUniquePublicTest"
	po.Println(testMessage)
	po.Flush()
	result := out.String()
	assert.Contains(t, result, testMessage)
}