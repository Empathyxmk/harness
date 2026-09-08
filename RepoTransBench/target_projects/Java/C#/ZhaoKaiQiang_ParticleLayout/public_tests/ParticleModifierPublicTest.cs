using Xunit;

namespace ZhaoKaiQiangParticleLayout.Tests.Public
{
    public interface IParticleModifier
    {
        void Apply(Particle particle, long milliseconds);
    }

    public class Particle
    {
        public float mCurrentY;
    }

    public class PublicParticleModifier : IParticleModifier
    {
        public void Apply(Particle particle, long milliseconds)
        {
            particle.mCurrentY = 44f;
        }
    }

    public class ParticleModifierPublicTest
    {
        [Fact]
        public void TestModifyPublic()
        {
            IParticleModifier m = new PublicParticleModifier();
            Particle p = new Particle();
            m.Apply(p, 100);
            Assert.Equal(44f, p.mCurrentY, 3);
        }
    }
}