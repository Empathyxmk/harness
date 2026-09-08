using System;
using Xunit;

namespace PublicTests
{
    public class EmojiUtilsPublicTests
    {
        [Fact]
        public void TestLoadEmojiUtilsClassPublic()
        {
            var type = Type.GetType("Binarywang.EmojiConverter.Util.EmojiUtils, Binarywang.EmojiConverter");
            Assert.NotNull(type);
        }
    }
}