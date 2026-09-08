using Xunit;
using AllenDowney.ThinkJavaCode;
using System.IO;

namespace OriginalTests.Ch03
{
    public class ConvertTest
    {
        [Fact]
        public void TestMainWithNumericInput()
        {
            var input = new StringReader("10\n");
            var originalIn = System.Console.In;
            var originalOut = System.Console.Out;
            var outputStream = new StringWriter();
            System.Console.SetIn(input);
            System.Console.SetOut(outputStream);

            try
            {
                Convert.Main(System.Array.Empty<string>());
            }
            catch
            {
                // ignore errors, just as in the Java test
            }
            finally
            {
                System.Console.SetIn(originalIn);
                System.Console.SetOut(originalOut);
            }
            var output = outputStream.ToString();
            Assert.Contains("miles", output.ToLower());
            Assert.Contains("kilometers", output.ToLower());
        }

        [Fact]
        public void TestMainWithInvalidInput()
        {
            var input = new StringReader("foo\n");
            var originalIn = System.Console.In;
            var originalOut = System.Console.Out;
            var outputStream = new StringWriter();
            System.Console.SetIn(input);
            System.Console.SetOut(outputStream);
            try
            {
                Convert.Main(System.Array.Empty<string>());
            }
            catch
            {
                // Ignore as in Java code
            }
            finally
            {
                System.Console.SetIn(originalIn);
                System.Console.SetOut(originalOut);
            }
            var output = outputStream.ToString();
            Assert.Contains("miles", output.ToLower());
        }
    }
}