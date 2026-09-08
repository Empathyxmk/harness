using Xunit;
using PocketSphinx;
using System.IO;

namespace PocketSphinxTests.Public
{
    public class SpeechRecognizerSetupPublicTests
    {
        [Fact]
        public void TestDefaultSetupReturnsSetupInstancePublic()
        {
            var setup = SpeechRecognizerSetup.DefaultSetup();
            Assert.NotNull(setup);
        }

        [Fact]
        public void TestSetupWithNonExistingFilesPublic()
        {
            var setup = SpeechRecognizerSetup.DefaultSetup();
            var acousticModel = new DirectoryInfo("dummy_model_dir_public");
            var dictionary = new FileInfo("dummy_dict_file_public.dic");
            var logDir = new DirectoryInfo("dummy_log_dir_public");

            Assert.Same(setup, setup.SetAcousticModel(acousticModel));
            Assert.Same(setup, setup.SetDictionary(dictionary));
            Assert.Same(setup, setup.SetRawLogDir(logDir));
        }

        [Fact]
        public void TestGetRecognizerReturnsInstancePublic()
        {
            var setup = SpeechRecognizerSetup.DefaultSetup();
            var recognizer = setup.GetRecognizer();
            Assert.NotNull(recognizer);
        }
    }
}