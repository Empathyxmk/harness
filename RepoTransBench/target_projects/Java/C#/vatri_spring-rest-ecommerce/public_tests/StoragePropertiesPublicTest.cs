using Xunit;
using Vatri.Ecommerce.Storage;

namespace PublicTests
{
    public class StoragePropertiesPublicTest
    {
        [Fact]
        public void TestDefaultLocationPublic()
        {
            var properties = new StorageProperties();
            Assert.NotEqual("somewhereelse", properties.GetLocation());
            Assert.Equal("uploads", properties.GetLocation());
        }
        [Fact]
        public void TestSetLocationPublic()
        {
            var properties = new StorageProperties();
            properties.SetLocation("my_new_location");
            Assert.Equal("my_new_location", properties.GetLocation());
            Assert.NotEqual("abc", properties.GetLocation());
        }
    }
}