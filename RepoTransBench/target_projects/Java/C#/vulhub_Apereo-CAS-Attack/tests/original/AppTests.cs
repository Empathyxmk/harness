using System;
using System.IO;
using Xunit;
using ApereoCasAttack;

namespace OriginalTests
{
    public class AppTests
    {
        [Fact]
        public void TestMainNoArgs()
        {
            var output = CaptureConsoleOutput(() => App.Main(Array.Empty<string>()));
            Assert.Contains("Hello from Apereo CAS Attack tool!", output);
        }

        [Fact]
        public void TestMainAttackCasTarget()
        {
            var output = CaptureConsoleOutput(() => App.Main(new string[] { "attack", "cas-server" }));
            Assert.Contains("Simulating CAS attack on cas-server", output);
        }

        [Fact]
        public void TestMainAttackNonCasTarget()
        {
            var output = CaptureConsoleOutput(() => App.Main(new string[] { "attack", "notcas" }));
            Assert.Contains("Simulating CAS attack on notcas", output);
        }

        [Fact]
        public void TestMainAttackNoTarget()
        {
            var output = CaptureConsoleOutput(() => App.Main(new string[] { "attack" }));
            Assert.Contains("No target specified for attack.", output);
        }

        [Fact]
        public void TestMainHelp()
        {
            var output = CaptureConsoleOutput(() => App.Main(new string[] { "help" }));
            Assert.Contains("Usage: java -jar apereo-cas-attack.jar", output);
        }

        [Fact]
        public void TestMainUnknownCommand()
        {
            var output = CaptureConsoleOutput(() => App.Main(new string[] { "unknown" }));
            Assert.Contains("Unknown command: unknown", output);
            Assert.Contains("Usage: java -jar apereo-cas-attack.jar", output);
        }

        [Fact]
        public void TestPerformAttackNull()
        {
            Assert.Equal("No target specified for attack.", App.PerformAttack(null));
        }

        [Fact]
        public void TestPerformAttackCasTarget()
        {
            Assert.Equal("Simulating CAS attack on cas-server", App.PerformAttack("cas-server"));
        }

        [Fact]
        public void TestPerformAttackNonCasTarget()
        {
            Assert.Equal("Target is not a CAS server: something", App.PerformAttack("something"));
        }

        [Fact]
        public void TestPerformAttackCasSubstringCaseInsensitive()
        {
            Assert.Equal("Target is not a CAS server: bestcASattack", App.PerformAttack("bestcASattack"));
        }

        private string CaptureConsoleOutput(Action act)
        {
            var sw = new StringWriter();
            var oldOut = Console.Out;
            Console.SetOut(sw);
            try
            {
                act();
            }
            finally
            {
                Console.SetOut(oldOut);
            }
            return sw.ToString();
        }
    }
}