using System.Collections.Generic;
using Xunit;

namespace PublicTests
{
    public class EnglishWordPublicTest
    {
        [Fact]
        public void TestConstructionAndPrintBeforeOtherValue()
        {
            var word = new EnglishWord(
                new List<Character> {
                    new Character('P'),
                    new Character('u'),
                    new Character('b'),
                    new Character('l'),
                    new Character('i'),
                    new Character('c')
                }
            );
            Assert.Equal(6, word.Count());
            word.PrintBefore();
            // Just a branch/coverage test for PrintBefore output
        }
    }
}