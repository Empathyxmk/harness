using System;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Original
{
    public class AJPFuzzerExtraTest
    {
        [Fact]
        public void TestMainRunsAndDoesNotFail()
        {
            // The main does nothing but can be invoked for coverage
            AJPFuzzer.Main(Array.Empty<string>());
        }
    }
}