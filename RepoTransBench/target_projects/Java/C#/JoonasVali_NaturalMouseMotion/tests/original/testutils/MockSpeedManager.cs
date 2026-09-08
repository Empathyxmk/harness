using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.TestUtils
{
    public class MockSpeedManager : SpeedManager
    {
        public override double GetSpeed(int distance)
        {
            return 1.0;
        }
    }
}