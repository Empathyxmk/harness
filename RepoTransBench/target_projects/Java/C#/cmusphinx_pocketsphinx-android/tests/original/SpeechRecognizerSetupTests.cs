using Xunit;
using PocketSphinx;
using System.IO;

namespace PocketSphinxTests.Original
{
    public class SpeechRecognizerSetupTests
    {
        [Fact]
        public void TestDefaultSetup()
        {
            var setup = SpeechRecognizerSetup.DefaultSetup();
            Assert.NotNull(setup);
        }

        [Fact]
        public void TestGetRecognizerReturnsSpeechRecognizer()
        {
            var setup = SpeechRecognizerSetup.DefaultSetup();
            setup.SetAcousticModel(new DirectoryInfo("."));
            setup.SetDictionary(new FileInfo("."));
            setup.SetRawLogDir(new DirectoryInfo("."));
            var recognizer = setup.GetRecognizer();
            Assert.NotNull(recognizer);
        }

        [Fact]
        public void TestSetKeyMethods()
        {
            var setup = SpeechRecognizerSetup.DefaultSetup();
            Assert.Equal(setup, setup.SetAcousticModel(new DirectoryInfo(".")));
            Assert.Equal(setup, setup.SetDictionary(new FileInfo(".")));
            Assert.Equal(setup, setup.SetRawLogDir(new DirectoryInfo(".")));
        }
    }
}