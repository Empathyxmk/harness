using Xunit;
using System.Collections.Generic;

namespace ZhaoKaiQiangParticleLayout.Tests.Public
{
    public class Context { }
    public class Particle
    {
        public float mCurrentX;
        public float mCurrentY;
    }
    public class ParticleField
    {
        public List<Particle> _particles = new();
        public ParticleField(Context ctx) { }
        public void SetParticles(List<Particle> particles) => _particles = particles;
    }

    public class ParticleFieldPublicTest
    {
        [Fact]
        public void TestSetParticlesPublic()
        {
            Context ctx = null;
            ParticleField field = new ParticleField(ctx);
            List<Particle> particles = new List<Particle>();
            Particle p = new Particle();
            particles.Add(p);
            field.SetParticles(particles);
            Assert.NotNull(field);
            Assert.Equal(1, particles.Count);
        }
    }
}