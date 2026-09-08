using System;
using Xunit;
using Binarywang.EmojiConverter;

namespace Tests.Original
{
    public class EmojiConverterEdgeTests
    {
        [Fact]
        public void TestNullInputToAlias()
        {
            var converter = EmojiConverter.GetInstance();
            Assert.Throws<ArgumentNullException>(() => converter.ToAlias(null));
        }

        [Fact]
        public void TestNullInputToUnicode()
        {
            var converter = EmojiConverter.GetInstance();
            Assert.Throws<ArgumentNullException>(() => converter.ToUnicode(null));
        }

        [Fact]
        public void TestEmptyString()
        {
            var converter = EmojiConverter.GetInstance();
            Assert.Equal("", converter.ToAlias(""));
            Assert.Equal("", converter.ToUnicode(""));
        }
    }
}