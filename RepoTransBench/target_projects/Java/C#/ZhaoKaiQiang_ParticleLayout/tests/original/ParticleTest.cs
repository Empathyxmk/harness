using Xunit;
using Moq;
using System.Collections.Generic;

namespace ZhaoKaiQiangParticleLayout.Tests.Original
{
    // Minimal stand-in classes for Particle, ParticleModifier, Bitmap, Canvas
    public class Bitmap
    {
        public virtual int Width => 10;
        public virtual int Height => 10;
    }
    public class Canvas { public virtual void DrawBitmap(Bitmap bmp, object matrix, object paint) { } }
    public interface IParticleModifier { void Apply(Particle particle, long milliseconds); }


    public class Particle
    {
        public float mScale = 1f;
        public int mAlpha = 255;
        public float mInitialX;
        public float mInitialY;
        public float mCurrentX;
        public float mCurrentY;
        public float mSpeedX;
        public float mSpeedY;
        public float mRotationSpeed;
        public long mStartingMiliseconds;
        private Bitmap _bitmap;
        private IList<IParticleModifier> _modifiers;

        public Particle() { }
        public Particle(Bitmap bitmap)
        {
            _bitmap = bitmap;
        }
        public void Init()
        {
            mScale = 1f;
            mAlpha = 255;
        }

        public void Configure(long life, float x, float y)
        {
            int w = _bitmap?.Width ?? 0;
            int h = _bitmap?.Height ?? 0;
            mInitialX = x - w / 2f;
            mInitialY = y - h / 2f;
            mCurrentX = mInitialX;
            mCurrentY = mInitialY;
        }

        public Particle Activate(long start, IList<IParticleModifier> modifiers)
        {
            mStartingMiliseconds = start;
            _modifiers = modifiers;
            return this;
        }

        public bool Update(long currentTime)
        {
            // expires if lifetime < currentTime - start
            if (_bitmap == null) return false;
            if ((currentTime - mStartingMiliseconds) > 100) return false;
            foreach (var m in _modifiers ?? new List<IParticleModifier>())
            {
                m.Apply(this, currentTime - mStartingMiliseconds);
            }
            // Move by speed
            mCurrentX += mSpeedX;
            mCurrentY += mSpeedY;
            return true;
        }

        public void Draw(Canvas canvas)
        {
            canvas.DrawBitmap(_bitmap, null, null);
        }
    }

    public class ParticleTest
    {
        private Mock<Bitmap> mockBitmap;
        private Mock<Canvas> mockCanvas;
        private Mock<IParticleModifier> mockModifier;
        private Particle particle;

        public ParticleTest()
        {
            mockBitmap = new Mock<Bitmap>();
            mockCanvas = new Mock<Canvas>();
            mockModifier = new Mock<IParticleModifier>();
            particle = new Particle(mockBitmap.Object);
            particle.Activate(0, new List<IParticleModifier> { mockModifier.Object });
        }

        [Fact]
        public void TestInitDefaults()
        {
            particle.Init();
            Assert.Equal(1f, particle.mScale, 3);
            Assert.Equal(255, particle.mAlpha);
        }

        [Fact]
        public void TestConfigureSetsFields()
        {
            mockBitmap.SetupGet(x => x.Width).Returns(10);
            mockBitmap.SetupGet(x => x.Height).Returns(20);
            particle.Configure(1000, 100f, 200f);

            Assert.Equal(95f, particle.mInitialX, 3);
            Assert.Equal(190f, particle.mInitialY, 3);
            Assert.Equal(95f, particle.mCurrentX, 3);
            Assert.Equal(190f, particle.mCurrentY, 3);
        }

        [Fact]
        public void TestUpdateReturnsFalseWhenExpired()
        {
            mockBitmap.SetupGet(x => x.Width).Returns(10);
            mockBitmap.SetupGet(x => x.Height).Returns(20);
            particle.Configure(100, 5, 5);
            bool active = particle.Update(200);
            Assert.False(active);
        }

        [Fact]
        public void TestUpdateMovesParticleAndCallsModifier()
        {
            mockBitmap.SetupGet(x => x.Width).Returns(10);
            mockBitmap.SetupGet(x => x.Height).Returns(10);
            particle.Activate(50, new List<IParticleModifier> { mockModifier.Object });
            particle.Configure(1000, 20f, 22f);
            particle.mSpeedX = 2f;
            particle.mSpeedY = 3f;
            particle.mRotationSpeed = 30f;
            bool active = particle.Update(60);
            Assert.True(active);
            mockModifier.Verify(m => m.Apply(It.IsAny<Particle>(), It.IsAny<long>()), Times.AtLeastOnce());
        }

        [Fact]
        public void TestActivateSetsStartTimeAndModifiers()
        {
            var mods = new List<IParticleModifier>();
            Particle result = particle.Activate(123L, mods);
            Assert.Equal(123L, particle.mStartingMiliseconds);
            Assert.Same(particle, result);
        }

        [Fact]
        public void TestDrawCallsCanvasDrawBitmap()
        {
            mockBitmap.SetupGet(x => x.Width).Returns(4);
            mockBitmap.SetupGet(x => x.Height).Returns(4);
            particle.Configure(1000, 2, 2);
            particle.Draw(mockCanvas.Object);
            mockCanvas.Verify(c => c.DrawBitmap(mockBitmap.Object, It.IsAny<object>(), It.IsAny<object>()), Times.AtLeastOnce());
        }
    }
}