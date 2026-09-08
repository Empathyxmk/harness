using System;
using System.IO;
using Xunit;

namespace PublicTests
{
    /// <summary>
    /// Public test for Writer with different sentence.
    /// </summary>
    public class WriterPublicTest : IDisposable
    {
        private StringWriter stdOutBuffer;
        private readonly TextWriter realStdOut = Console.Out;

        public WriterPublicTest()
        {
            stdOutBuffer = new StringWriter();
            Console.SetOut(stdOutBuffer);
        }

        public void Dispose()
        {
            Console.SetOut(realStdOut);
        }

        [Fact]
        public void SentenceByChinesePublic()
        {
            var writer = new Writer();
            TestWriterCn(writer.SentenceByChinese(), "我是来自北京的小明。");
        }

        [Fact]
        public void SentenceByEnglishPublic()
        {
            var writer = new Writer();
            TestWriterTrimmed(writer.SentenceByEnglish(), "I am a student from London.");
        }

        private void TestWriterTrimmed(CharacterComposite givenComposite, string expectedString)
        {
            var words = expectedString.Trim().Split(' ');
            Assert.NotNull(givenComposite);
            Assert.Equal(words.Length, givenComposite.Count());

            givenComposite.Print();

            var output = stdOutBuffer.ToString().Trim().ToLower();
            var expected = expectedString.Trim().ToLower();
            Assert.EndsWith(".", output);
            Assert.Equal(expected, output);
        }

        private void TestWriterCn(CharacterComposite givenComposite, string expectedString)
        {
            Assert.NotNull(givenComposite);

            givenComposite.Print();

            var output = stdOutBuffer.ToString().Trim();
            Assert.Contains("北京", output);
            Assert.EndsWith("。", output);
        }
    }
}