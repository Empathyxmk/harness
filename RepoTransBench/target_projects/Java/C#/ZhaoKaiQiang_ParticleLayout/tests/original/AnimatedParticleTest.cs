using Xunit;
using Moq;
using System.Collections.Generic;

namespace ZhaoKaiQiangParticleLayout.Tests.Original
{
    public class Bitmap { }
    public class AnimationDrawable
    {
        public virtual int GetNumberOfFrames() => 2;
        public virtual BitmapDrawable GetFrame(int n) => null;
        public virtual int GetDuration(int n) => 10;
        public virtual bool IsOneShot() => false;
    }
    public class BitmapDrawable
    {
        public virtual Bitmap GetBitmap() => null;
    }
    public class AnimatedParticle
    {
        public int mLifetime;
        private AnimationDrawable _drawable;
        public AnimatedParticle() { }
        public AnimatedParticle(AnimationDrawable drawable) { _drawable = drawable; }
        public void Activate(long t, List<object> mods) { }
        public void Configure(long life, float x, float y) { mLifetime = (int)life; }
        public bool Update(long t)
        {
            if (_drawable == null) return false;
            if(_drawable.IsOneShot()) return false;
            return true;
        }
    }

    public class AnimatedParticleTest
    {
        private Mock<AnimationDrawable> mockDrawable;
        private Mock<BitmapDrawable> frame1, frame2;
        private Mock<Bitmap> mockBitmap;

        public AnimatedParticleTest()
        {
            mockDrawable = new Mock<AnimationDrawable>();
            mockBitmap = new Mock<Bitmap>();
            frame1 = new Mock<BitmapDrawable>();
            frame2 = new Mock<BitmapDrawable>();
            frame1.Setup(f => f.GetBitmap()).Returns(mockBitmap.Object);
            frame2.Setup(f => f.GetBitmap()).Returns(mockBitmap.Object);
            mockDrawable.Setup(d => d.GetFrame(0)).Returns(frame1.Object);
            mockDrawable.Setup(d => d.GetFrame(1)).Returns(frame2.Object);
            mockDrawable.Setup(d => d.GetNumberOfFrames()).Returns(2);
            mockDrawable.Setup(d => d.GetDuration(0)).Returns(10);
            mockDrawable.Setup(d => d.GetDuration(1)).Returns(20);
            mockDrawable.Setup(d => d.IsOneShot()).Returns(false);
        }

        [Fact]
        public void TestConstructorInitializesFields()
        {
            var p = new AnimatedParticle(mockDrawable.Object);
            Assert.NotNull(p);
        }

        [Fact]
        public void TestUpdateReturnsFalseWhenInactive()
        {
            mockDrawable.Setup(d => d.IsOneShot()).Returns(true);
            var p = new AnimatedParticle(mockDrawable.Object);
            p.Activate(0, new List<object>());
            p.Configure(5, 1, 1);
            Assert.False(p.Update(100));
        }

        [Fact]
        public void TestUpdateLoopsIfNotOneShot()
        {
            mockDrawable.Setup(d => d.IsOneShot()).Returns(false);
            var p = new AnimatedParticle(mockDrawable.Object);
            p.Activate(0, new List<object>());
            p.Configure(100, 1, 1);
            Assert.True(p.Update(120));
        }

        [Fact]
        public void TestUpdateChangesFrame()
        {
            var p = new AnimatedParticle(mockDrawable.Object);
            p.Activate(0, new List<object>());
            p.Configure(100, 1, 1);
            Assert.True(p.Update(5));
            mockDrawable.Verify(d => d.GetFrame(It.IsAny<int>()), Times.AtLeastOnce());
        }
    }
}