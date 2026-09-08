using Xunit;
using Vatri.Ecommerce.Storage;

namespace OriginalTests
{
    public class StoragePropertiesTest
    {
        [Fact]
        public void TestDefaultLocation()
        {
            var properties = new StorageProperties();
            Assert.Equal("uploads", properties.GetLocation());
        }
        [Fact]
        public void TestSetLocation()
        {
            var properties = new StorageProperties();
            properties.SetLocation("abc");
            Assert.Equal("abc", properties.GetLocation());
        }
    }
}