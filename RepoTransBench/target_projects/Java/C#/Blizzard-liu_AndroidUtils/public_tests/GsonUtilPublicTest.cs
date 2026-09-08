using Xunit;

namespace AndroidUtils.PublicTests
{
    public class GsonUtilPublicTest
    {
        [Fact]
        public void TestNumberStringDeserialization_Public()
        {
            // Use different value
            string json = "123";
            int num = int.Parse(json);
            Assert.Equal(123, num);
        }
    }
}