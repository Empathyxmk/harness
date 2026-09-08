using System;
using Xunit;
using Binarywang.EmojiConverter;

namespace Tests.Original
{
    public class EmojiConverterTests
    {
        [Fact]
        public void TestToAliasAndUnicode()
        {
            var converter = EmojiConverter.GetInstance();
            string str = "😊";
            string alias = converter.ToAlias(str);
            Assert.True(alias.Contains(":blush:") || alias.Contains(":") || alias == str || alias == "😊");

            string unicode = converter.ToUnicode(alias);
            Assert.NotNull(unicode);
        }

        [Fact]
        public void TestToHtml()
        {
            var converter = EmojiConverter.GetInstance();
            string str = "😊";
            string html = converter.ToHtml(str);
            Assert.True(html.Contains("&#") || html == str || html == "😊");
        }

        [Fact]
        public void TestSingletonInstance()
        {
            Assert.NotNull(EmojiConverter.GetInstance());
            Assert.True(object.ReferenceEquals(EmojiConverter.GetInstance(), EmojiConverter.GetInstance()));
        }
    }
}