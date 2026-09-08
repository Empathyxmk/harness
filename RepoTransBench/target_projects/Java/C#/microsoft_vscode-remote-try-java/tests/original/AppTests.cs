using System;
using Xunit;
using MyCompany.App;

namespace OriginalTests
{
    public class AppTests
    {
        [Fact]
        public void TestGetMessage()
        {
            Assert.Equal("Hello Remote World!", App.GetMessage());
        }

        [Fact]
        public void TestEvaluateNumber_PositiveEven()
        {
            Assert.Equal("Positive Even", App.EvaluateNumber(2));
        }

        [Fact]
        public void TestEvaluateNumber_PositiveOdd()
        {
            Assert.Equal("Positive Odd", App.EvaluateNumber(3));
        }

        [Fact]
        public void TestEvaluateNumber_Negative()
        {
            Assert.Equal("Negative", App.EvaluateNumber(-7));
        }

        [Fact]
        public void TestEvaluateNumber_Zero()
        {
            Assert.Equal("Zero", App.EvaluateNumber(0));
        }
    }
}