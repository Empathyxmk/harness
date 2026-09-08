using Xunit;

namespace ZhaoKaiQiangParticleLayout.Tests.Public
{
    public class Particle
    {
        public float mCurrentX;
        public float mCurrentY;
    }

    public class ParticlePublicTest
    {
        [Fact]
        public void TestInitialValuesAreSetPublic()
        {
            Particle p = new Particle();
            p.mCurrentX = 15f;
            p.mCurrentY = 25f;
            Assert.Equal(15f, p.mCurrentX, 2);
            Assert.Equal(25f, p.mCurrentY, 2);
        }
    }
}