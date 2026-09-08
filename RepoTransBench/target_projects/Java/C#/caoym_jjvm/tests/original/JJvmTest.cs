using System;
using System.IO;
using Xunit;
using CaoymJjvm;

namespace CaoymJjvm.Tests.Original
{
    public class JJvmTest
    {
        [Fact]
        public void TestMainPrintsUsage()
        {
            var sysOut = Console.Out;
            var outStream = new StringWriter();
            Console.SetOut(outStream);

            try
            {
                JJvm.Main(Array.Empty<string>());
            }
            finally
            {
                Console.SetOut(sysOut);
            }

            var output = outStream.ToString();
            Assert.Contains("Usage: <classpath> <JJvm class> [args...]", output);
        }

        [Fact]
        public void TestMainHandlesException()
        {
            // Use fake classpath and class to provoke error in VM.
            var sysErr = Console.Error;
            var errStream = new StringWriter();
            Console.SetError(errStream);

            try
            {
                JJvm.Main(new string[] { "invalid", "NoSuchClass" });
            }
            finally
            {
                Console.SetError(sysErr);
            }

            var output = errStream.ToString();
            Assert.Contains("Exception", output);
        }
    }
}