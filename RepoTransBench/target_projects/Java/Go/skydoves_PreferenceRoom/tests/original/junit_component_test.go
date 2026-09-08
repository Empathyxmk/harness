package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type JunitComponent struct{}

func (jc *JunitComponent) TestProfile() interface{} {
	return struct{}{}
}
func (jc *JunitComponent) GetEntityNameList() []string {
	return []string{"TestProfile"}
}
func GetJunitComponentInstance() *JunitComponent {
	return &JunitComponent{}
}

func TestInjection(t *testing.T) {
	jc := GetJunitComponentInstance()
	assert.NotNil(t, jc)
	assert.NotNil(t, jc.TestProfile())
}

func TestJunitEntityList(t *testing.T) {
	jc := GetJunitComponentInstance()
	assert.Equal(t, "TestProfile", jc.GetEntityNameList()[0])
}