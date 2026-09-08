using System;
using System.Collections.Generic;
using System.IO;
using Xunit;

namespace Tests.Original
{
    public class EnglishSentenceTest
    {
        [Fact]
        public void TestConstructorAndPrintAfter()
        {
            var word = new EnglishWord(new List<Character>());
            var sentence = new EnglishSentence(new List<EnglishWord> { word });
            Assert.Equal(1, sentence.Count());
            var outsw = new StringWriter();
            var oldOut = Console.Out;
            Console.SetOut(outsw);
            sentence.PrintAfter();
            Console.SetOut(oldOut);
            Assert.Equal(".\n", outsw.ToString().Replace("\r\n", "\n"));
        }
    }
}