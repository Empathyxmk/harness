using System;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.TestUtils
{
    public class MockRandom : Random
    {
        public override int Next(int minValue, int maxValue)
        {
            return minValue; // always deterministic
        }
    }
}