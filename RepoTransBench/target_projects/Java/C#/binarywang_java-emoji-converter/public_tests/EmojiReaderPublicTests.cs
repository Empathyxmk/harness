using Xunit;
using Binarywang.EmojiConverter;

namespace PublicTests
{
    public class EmojiReaderPublicTests
    {
        [Fact]
        public void TestReadFromLocalPublic()
        {
            var reader = new EmojiReader();
            var obj = reader.Read(true);
            Assert.NotNull(obj);
        }

        [Fact]
        public void TestSb2UnicodeMapNotNullPublic()
        {
            var reader = new EmojiReader();
            Assert.NotNull(reader.GetSb2UnicodeMap());
        }
    }
}