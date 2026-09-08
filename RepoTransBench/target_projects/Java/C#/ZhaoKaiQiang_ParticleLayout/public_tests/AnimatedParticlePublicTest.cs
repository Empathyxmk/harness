using Xunit;

namespace ZhaoKaiQiangParticleLayout.Tests.Public
{
    public class AnimatedParticle
    {
        public int mLifetime;
    }

    public class AnimatedParticlePublicTest
    {
        [Fact]
        public void TestAnimatedParticleAnimationValuesPublic()
        {
            AnimatedParticle particle = new AnimatedParticle();
            particle.mLifetime = 3000;
            Assert.Equal(3000, particle.mLifetime);
        }
    }
}