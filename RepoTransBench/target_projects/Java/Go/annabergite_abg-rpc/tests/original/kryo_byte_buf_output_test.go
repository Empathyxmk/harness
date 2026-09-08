package tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ByteBuf struct {
	data []byte
	cap  int
}

func NewByteBuf(cap int) *ByteBuf {
	return &ByteBuf{data: make([]byte, 0, cap), cap: cap}
}
func (b *ByteBuf) WriteByte(bt byte) {
	b.data = append(b.data, bt)
}
func (b *ByteBuf) ReadableBytes() int {
	return len(b.data)
}

type ByteBufOutput struct {
	byteBuf *ByteBuf
}

func NewByteBufOutput(buf *ByteBuf) *ByteBufOutput {
	return &ByteBufOutput{byteBuf: buf}
}

func (o *ByteBufOutput) SetBuffer(buf *ByteBuf) {
	o.byteBuf = buf
}

func (o *ByteBufOutput) SetBufferWithCapacity(buf *ByteBuf, maxCapacity int) error {
	if maxCapacity < -1 {
		return errors.New("illegal argument")
	}
	o.byteBuf = buf
	return nil
}

func (o *ByteBufOutput) Write(b byte) {
	if o.byteBuf != nil {
		o.byteBuf.WriteByte(b)
	}
}
func (o *ByteBufOutput) Release() {
	o.byteBuf = nil
}

func TestConstructorSetBuffer(t *testing.T) {
	buf := NewByteBuf(8)
	out := NewByteBufOutput(buf)
	assert.NotNil(t, out)
	out.SetBuffer(nil)
}

func TestSetBufferWithCapacity(t *testing.T) {
	buf := NewByteBuf(8)
	out := NewByteBufOutput(buf)
	assert.NoError(t, out.SetBufferWithCapacity(buf, -1))
	err := out.SetBufferWithCapacity(buf, -2)
	assert.Error(t, err)
}

func TestWriteAndRelease(t *testing.T) {
	buf := NewByteBuf(4)
	out := NewByteBufOutput(buf)
	out.Write(65)
	assert.Equal(t, 1, buf.ReadableBytes())
	out.Release()
	assert.Nil(t, out.byteBuf)
}