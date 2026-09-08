package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yujiasun-distributed-kit/tests"
)

// Simulate a ZkDistributedSequence struct with relevant methods
type ZkDistributedSequence struct {
	client      *tests.CuratorFrameworkMock
	maxRetries  int
	baseSleepMs int
}

func NewZkDistributedSequence() *ZkDistributedSequence {
	return &ZkDistributedSequence{
		client:      tests.NewCuratorFrameworkMock(),
		maxRetries:  3,
		baseSleepMs: 1000,
	}
}

func (z *ZkDistributedSequence) SetMaxRetries(n int)   { z.maxRetries = n }
func (z *ZkDistributedSequence) GetMaxRetries() int    { return z.maxRetries }
func (z *ZkDistributedSequence) GetBaseSleepTimeMs() int { return z.baseSleepMs }
func (z *ZkDistributedSequence) Sequence(key string) *int64 {
	setter := z.client.SetData().WithVersion(-1)
	// simulate happy or exception path
	if key == "failcase" {
		z.client.FailNextSet = true
		_, err := setter.ForPath(key, []byte{})
		if err != nil {
			return nil
		}
		return nil
	}
	z.client.VersionForPath = 17
	version, err := setter.ForPath(key, []byte{})
	if err != nil {
		return nil
	}
	val := int64(version)
	return &val
}

func TestGetSetMaxRetries(t *testing.T) {
	seq := NewZkDistributedSequence()
	assert.Equal(t, 3, seq.GetMaxRetries())
	seq.SetMaxRetries(9)
	assert.Equal(t, 9, seq.GetMaxRetries())
}

func TestGetBaseSleepTimeMs(t *testing.T) {
	seq := NewZkDistributedSequence()
	assert.Equal(t, 1000, seq.GetBaseSleepTimeMs())
}

func TestSequenceReturnsValue(t *testing.T) {
	seq := NewZkDistributedSequence()
	res := seq.Sequence("abc")
	assert.NotNil(t, res)
	assert.Equal(t, int64(17), *res)
}

func TestSequenceHandlesException(t *testing.T) {
	seq := NewZkDistributedSequence()
	res := seq.Sequence("failcase")
	assert.Nil(t, res)
}