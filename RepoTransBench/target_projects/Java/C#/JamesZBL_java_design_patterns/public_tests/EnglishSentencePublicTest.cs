using System;
using System.Collections.Generic;
using System.IO;
using Xunit;

namespace PublicTests
{
    public class EnglishSentencePublicTest
    {
        [Fact]
        public void TestSentenceCompositionPublic()
        {
            var word1 = new EnglishWord(new List<Character> {
                new Character('T'), new Character('e'), new Character('s'), new Character('t')
            });
            var word2 = new EnglishWord(new List<Character> {
                new Character('P'), new Character('u'), new Character('b'), new Character('l'), new Character('i'), new Character('c')
            });
            var s = new EnglishSentence(new List<EnglishWord> { word1, word2 });
            Assert.Equal(2, s.Count());
            var baos = new StringWriter();
            var oldOut = Console.Out;
            Console.SetOut(baos);
            s.Print();
            Console.SetOut(oldOut);
            Assert.Contains(".", baos.ToString());
        }
    }
}