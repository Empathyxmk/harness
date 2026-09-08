using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Public
{
    public class AJPFuzzerExtraPublicTest
    {
        [Fact]
        public void TestMainHandlesArgs()
        {
            AJPFuzzer.Main(new string[] { "test", "case" });
        }
    }
}