using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class PreconditionsPublicTest
    {
        [Fact]
        public void TestCheckArgumentThrowsWithDifferentData()
        {
            var ex = Assert.Throws<System.ArgumentException>(() =>
            {
                Preconditions.CheckArgument(2 + 2 == 5, "Math doesn't work!");
            });
            Assert.Contains("Math doesn't work!", ex.Message);
        }

        [Fact]
        public void TestCheckNotNullThrowsWithDifferentData()
        {
            var ex = Assert.Throws<System.NullReferenceException>(() =>
            {
                Preconditions.CheckNotNull<object>(null, "Object must not be null!");
            });
            Assert.Contains("Object must not be null!", ex.Message);
        }
    }
}