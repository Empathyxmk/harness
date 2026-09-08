using System;
using System.IO;
using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.Tests
{
    public class OverloadingCalculation2Tests
    {
        [Fact]
        public void TestSumIntArgs()
        {
            OverloadingCalculation2 obj = new OverloadingCalculation2();
            var outStr = new StringWriter();
            var origOut = Console.Out;
            try
            {
                Console.SetOut(outStr);
                obj.Sum(1, 2);
            }
            finally
            {
                Console.SetOut(origOut);
            }
            Assert.Contains("int arg method invoked", outStr.ToString().Trim());
        }

        [Fact]
        public void TestSumLongArgs()
        {
            OverloadingCalculation2 obj = new OverloadingCalculation2();
            var outStr = new StringWriter();
            var origOut = Console.Out;
            try
            {
                Console.SetOut(outStr);
                obj.Sum(5L, 6L);
            }
            finally
            {
                Console.SetOut(origOut);
            }
            Assert.Contains("long arg method invoked", outStr.ToString().Trim());
        }
    }
}