using Xunit;
using Ch02Core.Parametrized;

namespace OriginalTests.Parametrized
{
    public class ParameterizedWithEnumSourceTest
    {
        private readonly WordCounter _wordCounter = new WordCounter();

        public enum Sentences
        {
            JUNIT_IN_ACTION,
            SOME_PARAMETERS,
            THREE_PARAMETERS
        }

        private string EnumToSentence(Sentences sentence)
        {
            return sentence switch
            {
                Sentences.JUNIT_IN_ACTION => "JUnit in Action",
                Sentences.SOME_PARAMETERS => "Check some parameters",
                Sentences.THREE_PARAMETERS => "Check three parameters",
                _ => ""
            };
        }

        [Theory]
        [InlineData(Sentences.JUNIT_IN_ACTION)]
        [InlineData(Sentences.SOME_PARAMETERS)]
        [InlineData(Sentences.THREE_PARAMETERS)]
        public void TestWordsInSentence(Sentences sentence)
        {
            Assert.Equal(3, _wordCounter.CountWords(EnumToSentence(sentence)));
        }

        [Theory]
        [InlineData(Sentences.JUNIT_IN_ACTION)]
        [InlineData(Sentences.THREE_PARAMETERS)]
        public void TestSelectedWordsInSentence(Sentences sentence)
        {
            Assert.Equal(3, _wordCounter.CountWords(EnumToSentence(sentence)));
        }

        [Theory]
        [InlineData(Sentences.JUNIT_IN_ACTION)]
        [InlineData(Sentences.SOME_PARAMETERS)]
        public void TestExcludedWordsInSentence(Sentences sentence)
        {
            Assert.Equal(3, _wordCounter.CountWords(EnumToSentence(sentence)));
        }
    }
}