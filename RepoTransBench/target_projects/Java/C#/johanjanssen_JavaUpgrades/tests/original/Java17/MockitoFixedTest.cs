using Xunit;
using Moq;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java17
{
    public class MockitoFixedTest
    {
        [Fact]
        public void TestEnumWithMethods()
        {
            var mock = new Mock<ExampleEnum>();
            var exampleEnum = mock.Object;
            Assert.NotNull(exampleEnum);
        }
    }
}