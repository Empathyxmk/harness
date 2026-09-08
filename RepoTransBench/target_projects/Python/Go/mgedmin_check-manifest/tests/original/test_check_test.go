package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type Metadata struct {
	Url             string
	Author          string
	AuthorEmail     string
	Name            string
	Version         string
	Description     string
	LongDescription string
}

func minimalMetadata() Metadata {
	return Metadata{
		Url:         "xxx",
		Author:      "xxx",
		AuthorEmail: "xxx",
		Name:        "xxx",
		Version:     "xxx",
	}
}

func (m *Metadata) isComplete() bool {
	return m.Url != "" && m.Author != "" && m.AuthorEmail != "" && m.Name != "" && m.Version != ""
}

func TestCheck_MetadataRequiredFields(t *testing.T) {
	empty := Metadata{}
	assert.False(t, empty.isComplete())
	all := minimalMetadata()
	assert.True(t, all.isComplete())
}