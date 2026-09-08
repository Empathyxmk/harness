using Xunit;
using Moq;
using System.Collections.Generic;

namespace ZhaoKaiQiangParticleLayout.Tests.Original
{
    // Minimal stubs
    public class Context { }
    public class AttributeSet { }
    public class Canvas { }
    public class Particle
    {
        public virtual void Draw(Canvas canvas) { }
    }
    public class ParticleField
    {
        public List<Particle> _particles = new();
        public ParticleField(Context ctx) { }
        public ParticleField(Context ctx, AttributeSet attrs) { }
        public ParticleField(Context ctx, AttributeSet attrs, int styleDef) { }
        public void SetParticles(List<Particle> particles) => _particles = particles;
        public void OnDraw(Canvas canvas)
        {
            foreach (var p in _particles)
                p.Draw(canvas);
        }
    }

    public class ParticleFieldTest
    {
        private Context mockContext;
        private AttributeSet mockAttrs;
        private Mock<Canvas> mockCanvas;

        public ParticleFieldTest()
        {
            mockContext = new Context();
            mockAttrs = new AttributeSet();
            mockCanvas = new Mock<Canvas>();
        }

        [Fact]
        public void TestConstructors()
        {
            ParticleField pf1 = new ParticleField(mockContext);
            ParticleField pf2 = new ParticleField(mockContext, mockAttrs);
            ParticleField pf3 = new ParticleField(mockContext, mockAttrs, 0);
        }

        [Fact]
        public void TestSetParticlesAndOnDraw()
        {
            ParticleField pf = new ParticleField(mockContext);
            var particle1 = new Mock<Particle>();
            var particle2 = new Mock<Particle>();
            List<Particle> particles = new List<Particle>
            {
                particle1.Object,
                particle2.Object
            };
            pf.SetParticles(particles);
            pf.OnDraw(mockCanvas.Object);
            particle1.Verify(p => p.Draw(It.IsAny<Canvas>()), Times.AtLeastOnce());
            particle2.Verify(p => p.Draw(It.IsAny<Canvas>()), Times.AtLeastOnce());
        }
    }
}