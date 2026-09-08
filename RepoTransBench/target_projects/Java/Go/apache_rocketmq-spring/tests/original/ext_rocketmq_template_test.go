package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ExtRocketMQTemplate struct{}

func TestExtRocketMQTemplateInstantiation(t *testing.T) {
	template := &ExtRocketMQTemplate{}
	assert.NotNil(t, template)
}