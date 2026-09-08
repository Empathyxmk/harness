using System;
using Xunit;

namespace PayatuDivaAndroid.PublicTests
{
    public class ExampleUnitPublicTests
    {
        [Fact]
        public void Simple_Addition_IsCorrect_Public()
        {
            Assert.Equal(24, 18 + 6);
            Assert.NotEqual(6, 36 / 5);
        }
    }
}