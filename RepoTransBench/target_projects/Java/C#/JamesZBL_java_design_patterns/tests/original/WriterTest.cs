using System;
using System.IO;
using Xunit;

namespace Tests.Original
{
    /// <summary>
    /// Test Writer sentence generator
    /// </summary>
    public class WriterTest : IDisposable
    {
        private StringWriter stdOutBuffer;
        private readonly TextWriter realStdOut = Console.Out;

        public WriterTest()
        {
            stdOutBuffer = new StringWriter();
            Console.SetOut(stdOutBuffer);
        }

        public void Dispose()
        {
            Console.SetOut(realStdOut);
        }

        [Fact]
        public void SentenceByChinese()
        {
            var writer = new Writer();
            TestWriterCn(writer.SentenceByChinese(), "我是来自北京的小明。");
        }

        [Fact]
        public void SentenceByEnglish()
        {
            var writer = new Writer();
            TestWriter(writer.SentenceByEnglish(), "I am a student from London.");
        }

        private void TestWriter(CharacterComposite givenComposite, string expectedString)
        {
            var words = expectedString.Trim().Split(' ');
            Assert.NotNull(givenComposite);
            Assert.Equal(givenComposite.Count(), words.Length);

            givenComposite.Print();

            Assert.Equal(expectedString, stdOutBuffer.ToString().Trim());
        }

        private void TestWriterCn(CharacterComposite givenComposite, string expectedString)
        {
            Assert.NotNull(givenComposite);

            givenComposite.Print();

            Assert.Equal(expectedString, stdOutBuffer.ToString().Trim());
        }
    }
}