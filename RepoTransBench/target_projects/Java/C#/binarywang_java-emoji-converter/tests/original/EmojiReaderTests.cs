using Xunit;
using Binarywang.EmojiConverter;

namespace Tests.Original
{
    public class EmojiReaderTests
    {
        [Fact]
        public void TestClassLoads()
        {
            // Ensure the class can be loaded (utility class)
            Assert.NotNull(typeof(EmojiReader));
        }
    }
}