using Xunit;
using Ch02Core.Parametrized;

namespace OriginalTests.Parametrized
{
    public class ParameterizedWithValueSourceTest
    {
        private readonly WordCounter _wordCounter = new WordCounter();

        [Theory]
        [InlineData("Check three parameters")]
        [InlineData("JUnit in Action")]
        public void TestWordsInSentence(string sentence)
        {
            Assert.Equal(3, _wordCounter.CountWords(sentence));
        }
    }
}