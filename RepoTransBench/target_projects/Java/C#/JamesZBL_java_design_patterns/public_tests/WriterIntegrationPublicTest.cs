using System;
using System.IO;
using Xunit;

namespace PublicTests
{
    public class WriterIntegrationPublicTest
    {
        [Fact]
        public void TestWriterSentencesPublic()
        {
            var output = new StringWriter();
            var oldOut = Console.Out;
            Console.SetOut(output);
            new Writer().SentenceByEnglish().Print();
            Console.SetOut(oldOut);
            string result = output.ToString();
            Assert.Contains("student", result);
            Assert.Contains("from", result);
        }
    }
}