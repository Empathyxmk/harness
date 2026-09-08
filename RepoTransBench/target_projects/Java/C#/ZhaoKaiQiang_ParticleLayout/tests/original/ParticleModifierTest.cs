using Xunit;

namespace ZhaoKaiQiangParticleLayout.Tests.Original
{
    public interface IParticleModifier
    {
        void Apply(object particle, long milliseconds);
    }

    public class Particle
    {
    }

    public class ParticleModifierTest
    {
        [Fact]
        public void TestApplyNoop()
        {
            var p = new Particle();
            IParticleModifier modifier = new NoopModifier();
            modifier.Apply(p, 10L);
        }

        private class NoopModifier : IParticleModifier
        {
            public void Apply(object particle, long milliseconds) { }
        }
    }
}