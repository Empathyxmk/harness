using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigFormatterPublicTests
    {
        [Fact]
        public void TestFormatKeepsInputWhenNoTwig()
        {
            var formatter = new TwigFormatter();
            string input = "<h2>No Twig public!</h2>";
            Assert.Equal(input, formatter.Format(input));
        }

        [Fact]
        public void TestFormatHandlesTwigBlock()
        {
            var formatter = new TwigFormatter();
            string input = "{% for item in items %}<li>{{ item }}</li>{% endfor %}";
            string formatted = formatter.Format(input);
            Assert.NotNull(formatted);
            Assert.False(string.IsNullOrEmpty(formatted));
        }
    }
}