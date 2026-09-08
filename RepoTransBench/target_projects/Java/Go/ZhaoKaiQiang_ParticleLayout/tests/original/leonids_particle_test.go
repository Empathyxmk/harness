package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Particle and its dependencies
type BitmapMock struct {
	width, height int
}

func (b *BitmapMock) Width() int  { return b.width }
func (b *BitmapMock) Height() int { return b.height }

type CanvasMock struct {
	drawBitmapCalled bool
}

func (c *CanvasMock) DrawBitmap(b *BitmapMock) {
	c.drawBitmapCalled = true
}

type ParticleModifier interface {
	Apply(p *Particle, ms int64)
}

type ParticleModifierMock struct {
	AppliedCalls []int64
}

func (m *ParticleModifierMock) Apply(p *Particle, ms int64) {
	m.AppliedCalls = append(m.AppliedCalls, ms)
}

type Particle struct {
	mScale               float32
	mAlpha               int
	mInitialX, mInitialY float32
	mCurrentX, mCurrentY float32
	mSpeedX, mSpeedY     float32
	mRotationSpeed       float32
	mStartingMiliseconds int64
	modifiers            []ParticleModifier
	bitmap               *BitmapMock
}

func NewParticle(bmp *BitmapMock) *Particle {
	return &Particle{
		bitmap:   bmp,
		mScale:   1,
		mAlpha:   255,
		modifiers: []ParticleModifier{},
	}
}

func (p *Particle) Init() {
	p.mScale = 1.0
	p.mAlpha = 255
}

func (p *Particle) Configure(lifetime int, x, y float32) {
	w := float32(p.bitmap.Width())
	h := float32(p.bitmap.Height())
	p.mInitialX = x - w/2
	p.mInitialY = y - h/2
	p.mCurrentX = p.mInitialX
	p.mCurrentY = p.mInitialY
}

func (p *Particle) Update(ms int64) bool {
	// Simulate lifetime expiry logic
	if ms > 100 {
		return false
	}
	if len(p.modifiers) > 0 {
		for _, m := range p.modifiers {
			m.Apply(p, ms)
		}
	}
	p.mCurrentX += p.mSpeedX
	p.mCurrentY += p.mSpeedY
	return true
}

func (p *Particle) Activate(startMs int64, mods []ParticleModifier) *Particle {
	p.mStartingMiliseconds = startMs
	p.modifiers = mods
	return p
}

func (p *Particle) Draw(c *CanvasMock) {
	c.DrawBitmap(p.bitmap)
}

func TestParticle_InitDefaults(t *testing.T) {
	bmp := &BitmapMock{}
	p := NewParticle(bmp)
	p.Init()
	assert.Equal(t, float32(1.0), p.mScale)
	assert.Equal(t, 255, p.mAlpha)
}

func TestParticle_ConfigureSetsFields(t *testing.T) {
	bmp := &BitmapMock{width: 10, height: 20}
	p := NewParticle(bmp)
	p.Configure(1000, 100, 200)
	assert.InDelta(t, 95.0, float64(p.mInitialX), 0.001)
	assert.InDelta(t, 190.0, float64(p.mInitialY), 0.001)
	assert.InDelta(t, 95.0, float64(p.mCurrentX), 0.001)
	assert.InDelta(t, 190.0, float64(p.mCurrentY), 0.001)
}

func TestParticle_UpdateReturnsFalseWhenExpired(t *testing.T) {
	bmp := &BitmapMock{width: 10, height: 20}
	p := NewParticle(bmp)
	p.Configure(100, 5, 5)
	active := p.Update(200)
	assert.False(t, active)
}

func TestParticle_UpdateMovesParticleAndCallsModifier(t *testing.T) {
	bmp := &BitmapMock{width: 10, height: 10}
	mod := &ParticleModifierMock{}
	p := NewParticle(bmp)
	p.Activate(50, []ParticleModifier{mod})
	p.Configure(1000, 20.0, 22.0)
	p.mSpeedX = 2.0
	p.mSpeedY = 3.0
	p.mRotationSpeed = 30.0
	active := p.Update(60)
	assert.True(t, active)
	if len(mod.AppliedCalls) == 0 {
		t.Error("Particle modifier was not applied")
	}
}

func TestParticle_ActivateSetsStartTimeAndModifiers(t *testing.T) {
	bmp := &BitmapMock{}
	p := NewParticle(bmp)
	var mods []ParticleModifier
	r := p.Activate(123, mods)
	assert.Equal(t, int64(123), p.mStartingMiliseconds)
	assert.Equal(t, p, r)
}

func TestParticle_DrawCallsCanvasDrawBitmap(t *testing.T) {
	bmp := &BitmapMock{width: 4, height: 4}
	p := NewParticle(bmp)
	canvas := &CanvasMock{}
	p.Configure(1000, 2, 2)
	p.Draw(canvas)
	if !canvas.drawBitmapCalled {
		t.Error("Canvas.DrawBitmap was not called")
	}
}