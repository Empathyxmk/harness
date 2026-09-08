using System;
using Xunit;
using MyCompany.App;

namespace PublicTests
{
    public class AppPublicTests
    {
        [Fact]
        public void TestGetMessage_Public()
        {
            Assert.Equal("Hello Remote World!", App.GetMessage());
        }

        [Fact]
        public void TestEvaluateNumber_PositiveEven_Public()
        {
            Assert.Equal("Positive Even", App.EvaluateNumber(8));
        }

        [Fact]
        public void TestEvaluateNumber_PositiveOdd_Public()
        {
            Assert.Equal("Positive Odd", App.EvaluateNumber(15));
        }

        [Fact]
        public void TestEvaluateNumber_Negative_Public()
        {
            Assert.Equal("Negative", App.EvaluateNumber(-123));
        }

        [Fact]
        public void TestEvaluateNumber_Zero_Public()
        {
            Assert.Equal("Zero", App.EvaluateNumber(0));
        }
    }
}