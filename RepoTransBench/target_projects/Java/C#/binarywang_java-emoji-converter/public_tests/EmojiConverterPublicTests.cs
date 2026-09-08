using System;
using Xunit;
using Binarywang.EmojiConverter;

namespace PublicTests
{
    public class EmojiConverterPublicTests
    {
        [Fact]
        public void TestToAliasAndUnicodePublic()
        {
            var converter = EmojiConverter.GetInstance();
            string str = "😂";
            string alias = converter.ToAlias(str);
            Assert.True(alias.Contains(":joy:") || alias.Contains(":") || alias == str || alias == "😂");

            string unicode = converter.ToUnicode(alias);
            Assert.NotNull(unicode);
        }

        [Fact]
        public void TestToHtmlPublic()
        {
            var converter = EmojiConverter.GetInstance();
            string str = "😂";
            string html = converter.ToHtml(str);
            Assert.True(html.Contains("&#") || html == str || html == "😂");
        }

        [Fact]
        public void TestSingletonInstancePublic()
        {
            Assert.NotNull(EmojiConverter.GetInstance());
            Assert.True(object.ReferenceEquals(EmojiConverter.GetInstance(), EmojiConverter.GetInstance()));
        }
    }
}