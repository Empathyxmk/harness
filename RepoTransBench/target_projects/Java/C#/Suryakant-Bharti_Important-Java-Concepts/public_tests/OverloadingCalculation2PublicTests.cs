using System;
using System.IO;
using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.PublicTests
{
    public class OverloadingCalculation2PublicTests
    {
        [Fact]
        public void TestSumIntArgs()
        {
            var obj = new OverloadingCalculation2();
            var outStr = new StringWriter();
            var origOut = Console.Out;
            try
            {
                Console.SetOut(outStr);
                obj.Sum(8, 13);
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
            var obj = new OverloadingCalculation2();
            var outStr = new StringWriter();
            var origOut = Console.Out;
            try
            {
                Console.SetOut(outStr);
                obj.Sum(13L, 22L);
            }
            finally
            {
                Console.SetOut(origOut);
            }
            Assert.Contains("long arg method invoked", outStr.ToString().Trim());
        }
    }
}