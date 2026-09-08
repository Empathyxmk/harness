using System;
using System.IO;
using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.Tests
{
    public class ManualMainTests
    {
        [Fact]
        public void TestAdderMainManual()
        {
            Assert.Equal(22, Adder.Add(11, 11));
            Assert.Equal(24.9, Adder.Add(12.3, 12.6), 9);
        }

        [Fact]
        public void TestExampleOverloadingMainManual()
        {
            var outStr = new StringWriter();
            var origOut = Console.Out;
            try
            {
                Console.SetOut(outStr);
                ExampleOverloading.Main(Array.Empty<string>());
            }
            finally
            {
                Console.SetOut(origOut);
            }
            var output = outStr.ToString();
            Assert.Contains("Minimum Value = 6", output);
            Assert.Contains("Minimum Value = 7.3", output);
        }

        [Fact]
        public void TestOverloadingCalculation2Main()
        {
            var outStr = new StringWriter();
            var origOut = Console.Out;
            try
            {
                Console.SetOut(outStr);
                OverloadingCalculation2.Main(Array.Empty<string>());
            }
            finally
            {
                Console.SetOut(origOut);
            }
            var output = outStr.ToString();
            Assert.Contains("int arg method invoked", output);
        }
    }
}