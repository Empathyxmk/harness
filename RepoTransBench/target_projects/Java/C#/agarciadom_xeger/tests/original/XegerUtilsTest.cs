using System;
using Xunit;

namespace XegerLib.Tests.Original
{
    public class XegerUtilsTest
    {
        [Fact]
        public void ShouldGenerateRandomNumberCorrectly()
        {
            var random = new Random();
            for (int i = 0; i < 100; i++)
            {
                int number = Xeger.GetRandomInt(3, 7, random);
                Assert.InRange(number, 3, 7);
            }
        }
    }
}