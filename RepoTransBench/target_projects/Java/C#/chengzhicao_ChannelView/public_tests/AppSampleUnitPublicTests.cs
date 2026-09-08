using Xunit;

namespace PublicTests
{
    public class AppSampleUnitPublicTests
    {
        [Fact]
        public void Subtraction_IsCorrect()
        {
            Assert.Equal(2, 5 - 3);
        }
    }
}