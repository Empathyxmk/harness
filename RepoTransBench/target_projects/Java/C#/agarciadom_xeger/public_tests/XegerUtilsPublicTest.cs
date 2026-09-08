using System;
using Xunit;

namespace XegerLib.Tests.Public
{
    public class XegerUtilsPublicTest
    {
        [Fact]
        public void ShouldGenerateRandomNumberCorrectly()
        {
            var random = new Random();
            for (int i = 0; i < 100; i++)
            {
                int number = Xeger.GetRandomInt(8, 11, random);
                Assert.InRange(number, 8, 11);
            }
        }
    }
}