using System;
using System.IO;
using Xunit;

namespace Tests.Original
{
    public class WriterIntegrationTest
    {
        [Fact]
        public void TestWriterSentences()
        {
            var output = new StringWriter();
            var oldOut = Console.Out;
            Console.SetOut(output);
            // You must implement the Writer class in src/MainProject mimicking Java's logic
            new Writer().SentenceByChinese().Print();
            new Writer().SentenceByEnglish().Print();
            Console.SetOut(oldOut);
            string result = output.ToString();
            Assert.Contains(".", result);
        }
    }
}