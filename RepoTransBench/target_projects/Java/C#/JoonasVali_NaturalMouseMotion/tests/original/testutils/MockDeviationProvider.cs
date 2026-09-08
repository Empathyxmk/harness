using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.TestUtils
{
    public class MockDeviationProvider : DeviationProvider
    {
        public override double GetDeviation()
        {
            return 0.1;
        }
    }
}