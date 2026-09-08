using Xunit;
using GBByPass;
using System.IO;
using System;

namespace Tests.Original
{
    public class MainFullCoverageTest
    {
        [Fact]
        public void TestMainWithNoArgs()
        {
            var sw = new StringWriter();
            var original = Console.Out;
            Console.SetOut(sw);

            Main.MainEntry(new string[] { });

            Console.SetOut(original);
            string output = sw.ToString();
            Assert.True(output.Length > 0);
        }

        [Fact]
        public void TestMainWithNormalArg()
        {
            var sw = new StringWriter();
            var original = Console.Out;
            Console.SetOut(sw);

            Main.MainEntry(new string[] { "4567" });

            Console.SetOut(original);
            string output = sw.ToString();
            Assert.True(output.Length > 0);
        }

        [Fact]
        public void TestMainWithAlphaArg()
        {
            var sw = new StringWriter();
            var original = Console.Out;
            Console.SetOut(sw);

            Main.MainEntry(new string[] { "abc123" });

            Console.SetOut(original);
            string output = sw.ToString();
            Assert.True(output.Length > 0);
        }

        [Fact]
        public void TestMainWithEmptyArg()
        {
            var sw = new StringWriter();
            var original = Console.Out;
            Console.SetOut(sw);

            Main.MainEntry(new string[] { "" });

            Console.SetOut(original);
            string output = sw.ToString();
            Assert.True(output.Length > 0);
        }
    }
}