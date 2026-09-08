using System;
using System.IO;
using Xunit;
using Cybereason_Logout4Shell;

namespace PublicTests
{
    public class Log4jPublicTest : IDisposable
    {
        private StringWriter outWriter;
        private StringWriter errWriter;
        private TextWriter originalOut;
        private TextWriter originalErr;

        public Log4jPublicTest()
        {
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
            Log4j.ThreadContext["header"] = "PUBLIC_HEADER";
            // Write error to output as in test
            Console.WriteLine($"{Log4j.ThreadContext["header"]}: Another error!");
            string output = outWriter.ToString();
            Assert.Contains("PUBLIC_HEADER", output);
            Assert.Contains("Another error!", output);
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
            // Check for presence of "ldap://127.0.0.1:1389" and "${jndi:" as in the Java public test
            Assert.Contains("ldap://127.0.0.1:1389", output);
            Assert.Contains("${jndi:", output);
        }
    }
}