using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Public
{
    public class AJPFuzzerPublicTest
    {
        [Fact]
        public void TestMainNoCrash()
        {
            AJPFuzzer.Main(new string[] { "--version" });
            AJPFuzzer.Main(new string[0]);
        }
    }
}