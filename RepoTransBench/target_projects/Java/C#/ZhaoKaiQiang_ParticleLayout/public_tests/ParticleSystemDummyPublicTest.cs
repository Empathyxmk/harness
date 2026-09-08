using Xunit;

namespace ZhaoKaiQiangParticleLayout.Tests.Public
{
    // Stub for the system
    public class ParticleSystem
    {
        public long mCurrentTime;
        public ParticleSystem(object a, int b, object d, long duration)
        {
            // No real implementation needed
        }
        public void Update(long time)
        {
            mCurrentTime = time;
        }
    }

    public class ParticleSystemDummyPublicTest
    {
        [Fact]
        public void TestUpdateTimeProgressionPublic()
        {
            ParticleSystem ps = new ParticleSystem(null, 10, null, 3000);
            long startTime = 1000L;
            ps.mCurrentTime = startTime;
            ps.Update(startTime + 300);
            Assert.Equal(1300L, ps.mCurrentTime);
        }
    }
}