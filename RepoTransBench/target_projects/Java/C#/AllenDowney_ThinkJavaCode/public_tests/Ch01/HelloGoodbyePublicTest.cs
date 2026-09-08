using Xunit;
using AllenDowney.ThinkJavaCode;
using System.IO;

namespace PublicTests.Ch01
{
    public class HelloGoodbyePublicTest
    {
        [Fact]
        public void TestHelloMainOutputDifferentData()
        {
            var outStream = new StringWriter();
            System.Console.SetOut(outStream);
            Hello.Main(System.Array.Empty<string>());
            string output = outStream.ToString().Trim();
            Assert.True(output.StartsWith("Hello") || output.Contains("Hello"));
            Assert.True(output.Contains("Goodbye"));
        }
    }
}