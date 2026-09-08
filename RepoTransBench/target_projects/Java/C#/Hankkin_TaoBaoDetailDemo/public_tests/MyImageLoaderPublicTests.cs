using Xunit;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Public.Tests
{
    public class MyImageLoaderPublicTests
    {
        [Fact]
        public void PublicSingletonInstanceDifferentCallNotNull()
        {
            var instanceA = MyImageLoader.GetInstance();
            var instanceB = MyImageLoader.GetInstance();
            Assert.NotNull(instanceA);
            Assert.NotNull(instanceB);
            Assert.True(ReferenceEquals(instanceA, instanceB));
        }
    }
}