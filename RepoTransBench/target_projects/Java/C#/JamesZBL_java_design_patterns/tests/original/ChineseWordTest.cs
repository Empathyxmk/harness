using System;
using System.Collections.Generic;
using System.IO;
using Xunit;

namespace Tests.Original
{
    public class ChineseWordTest
    {
        [Fact]
        public void TestConstructorAndPrintBefore()
        {
            var c = new Character(delegate { });
            var word = new ChineseWord(new List<Character> { c });
            Assert.Equal(1, word.Count());
            var outsw = new StringWriter();
            var oldOut = Console.Out;
            Console.SetOut(outsw);
            word.PrintBefore();
            Console.SetOut(oldOut);
            Assert.Equal("", outsw.ToString());
        }
    }
}