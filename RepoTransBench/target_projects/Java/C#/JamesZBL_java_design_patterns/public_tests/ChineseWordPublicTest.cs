using System.Collections.Generic;
using Xunit;

namespace PublicTests
{
    public class ChineseWordPublicTest
    {
        [Fact]
        public void TestChineseWordWithOtherCharacters()
        {
            // Use different Chinese characters for a public test ("我们" meaning "we")
            var c1 = new Character('我');
            var c2 = new Character('们');
            var word = new ChineseWord(new List<Character> { c1, c2 });
            Assert.Equal(2, word.Count());
        }
    }
}