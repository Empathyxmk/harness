using Xunit;
using PocketSphinx;

namespace PocketSphinxTests.Public
{
    public class SpeechRecognizerPublicTests
    {
        [Fact]
        public void TestSpeechRecognizerInstancePublic()
        {
            var recognizer = new SpeechRecognizer();
            Assert.NotNull(recognizer);
        }

        // Additional public tests can be added here if needed.
    }
}