using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.TestUtils
{
    public class MockNoiseProvider : NoiseProvider
    {
        public override double GetNoise()
        {
            return 0.05;
        }
    }
}