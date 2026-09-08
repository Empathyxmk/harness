package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type Distribution struct {
	CommandPackages []string
}

func (d *Distribution) GetCommandPackages() []string {
	if d.CommandPackages == nil {
		return []string{"distutils.command"}
	}
	return append([]string{"distutils.command"}, d.CommandPackages...)
}

func TestDistribution_CommandPackages(t *testing.T) {
	dist := Distribution{}
	cp := dist.GetCommandPackages()
	assert.Equal(t, []string{"distutils.command"}, cp)

	dist.CommandPackages = []string{"foo.bar", "splat"}
	cp = dist.GetCommandPackages()
	assert.Equal(t, []string{"distutils.command", "foo.bar", "splat"}, cp)
}