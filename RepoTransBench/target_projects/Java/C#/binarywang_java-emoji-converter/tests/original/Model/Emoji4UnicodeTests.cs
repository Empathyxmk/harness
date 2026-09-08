using Xunit;
using Binarywang.EmojiConverter.Model;

namespace Tests.Original.Model
{
    public class Emoji4UnicodeTests
    {
        [Fact]
        public void TestToStringAndClassLoads()
        {
            var emoji = new Emoji4Unicode();
            Assert.NotNull(emoji.ToString());
            Assert.NotNull(typeof(Emoji4Unicode));
        }
    }
}