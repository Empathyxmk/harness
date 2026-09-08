using Xunit;
using Binarywang.EmojiConverter.Model;

namespace PublicTests.Model
{
    public class Emoji4UnicodePublicTests
    {
        [Fact]
        public void TestEmoji4UnicodePublicSettersAndGetters()
        {
            var unicode = new Emoji4Unicode();
            unicode.SetCategories(null);
            Assert.Null(unicode.GetCategories());
        }
    }
}