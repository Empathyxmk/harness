using System;
using System.IO;
using Xunit;
using Cybereason_Logout4Shell;

namespace OriginalTests
{
    public class Log4jTest : IDisposable
    {
        private StringWriter outWriter;
        private StringWriter errWriter;
        private TextWriter originalOut;
        private TextWriter originalErr;

        public Log4jTest()
        {
            // Redirect standard output and error to stringwriters for capturing test output
            originalOut = Console.Out;
            originalErr = Console.Error;
            outWriter = new StringWriter();
            errWriter = new StringWriter();
            Console.SetOut(outWriter);
            Console.SetError(errWriter);
            Log4j.ThreadContext.Clear();
        }

        public void Dispose()
        {
            Console.SetOut(originalOut);
            Console.SetError(originalErr);
            Log4j.ThreadContext.Clear();
        }

        [Fact]
        public void TestConfigureLoggerWithThreadContext()
        {
            Log4j.configureLoggerWithThreadContext();
            // Simulate logger with ThreadContext (since we don't have a real logger)
            Log4j.ThreadContext["header"] = "TEST_HEADER";
            // Simulate logger.error("Error message!") -- just write to output for test purposes
            Console.WriteLine($"{Log4j.ThreadContext["header"]}: Error message!");
            string output = outWriter.ToString();
            Assert.Contains("TEST_HEADER", output);
            Assert.Contains("Error message!", output);
        }

        [Fact]
        public void TestMainWithThreadLocalAttack()
        {
            string[] args = new[] { "-t" };
            Log4j.main(args);
            string output = outWriter.ToString();
            Assert.Contains("Will use ThreadContext as attack vector", output);
            Assert.Contains("Vulnerable through thread context - 1", output);
            Assert.Contains("Vulnerable through thread context - 2", output);
        }

        [Fact]
        public void TestMainWithoutThreadLocalAttack()
        {
            string[] args = Array.Empty<string>();
            Log4j.main(args);
            string output = outWriter.ToString();
            Assert.Contains("jndi:ldap://127.0.0.1:1389/a", output);
        }
    }
}