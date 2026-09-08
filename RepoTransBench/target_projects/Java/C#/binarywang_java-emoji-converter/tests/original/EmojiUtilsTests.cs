using System;
using Xunit;

namespace Tests.Original
{
    public class EmojiUtilsTests
    {
        [Fact]
        public void TestLoadEmojiUtilsClass()
        {
            // Just ensure the class can be loaded
            var type = Type.GetType("Binarywang.EmojiConverter.Util.EmojiUtils, Binarywang.EmojiConverter");
            Assert.NotNull(type);
        }
    }
}