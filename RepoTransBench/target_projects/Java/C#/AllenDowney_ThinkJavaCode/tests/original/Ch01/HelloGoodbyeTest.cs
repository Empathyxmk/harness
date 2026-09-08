using Xunit;
using AllenDowney.ThinkJavaCode;
using System.IO;

namespace OriginalTests.Ch01
{
    public class HelloGoodbyeTest
    {
        [Fact]
        public void TestHelloOutput()
        {
            var originalOut = System.Console.Out;
            var baos = new StringWriter();
            System.Console.SetOut(baos);
            Hello.Main(System.Array.Empty<string>());
            System.Console.SetOut(originalOut);
            var output = baos.ToString().Trim();
            Assert.Equal("Hello, World!", output);
        }

        [Fact]
        public void TestGoodbyeOutput()
        {
            var originalOut = System.Console.Out;
            var baos = new StringWriter();
            System.Console.SetOut(baos);
            Goodbye.Main(System.Array.Empty<string>());
            System.Console.SetOut(originalOut);
            var output = baos.ToString().Replace("\r", "").Trim();
            Assert.Equal("Goodbye, cruel world", output);
        }
    }
}