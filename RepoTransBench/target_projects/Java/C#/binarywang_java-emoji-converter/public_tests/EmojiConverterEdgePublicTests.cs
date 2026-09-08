using System;
using Xunit;
using Binarywang.EmojiConverter;

namespace PublicTests
{
    public class EmojiConverterEdgePublicTests
    {
        [Fact]
        public void TestNullInputToAliasPublic()
        {
            var converter = EmojiConverter.GetInstance();
            Assert.Throws<ArgumentNullException>(() => converter.ToAlias(null));
        }

        [Fact]
        public void TestNullInputToUnicodePublic()
        {
            var converter = EmojiConverter.GetInstance();
            Assert.Throws<ArgumentNullException>(() => converter.ToUnicode(null));
        }

        [Fact]
        public void TestWhitespaceString()
        {
            var converter = EmojiConverter.GetInstance();
            Assert.Equal(" ", converter.ToAlias(" "));
            Assert.Equal(" ", converter.ToUnicode(" "));
        }
    }
}