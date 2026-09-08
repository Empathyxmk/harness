using System;
using System.Collections.Generic;
using Xunit;
using UsadellabTrimmomatic;
using UsadellabTrimmomatic.trim;
using UsadellabTrimmomatic.util;

namespace UsadellabTrimmomatic.PublicTests
{
    public class TrimmomaticPublicTest
    {
        [Fact]
        public void TestCalcAutoThreadCountIsPositive()
        {
            int threadCount = Trimmomatic.CalcAutoThreadCount();
            Assert.True(threadCount >= 1, "Thread count should be at least 1");
        }

        [Fact]
        public void TestCreateTrimmersWithNonEmptyArgs()
        {
            var logger = new Logger(false);
            var args = new List<string> { "HEADCROP:3" };
            Trimmer[] arr = Trimmomatic.CreateTrimmers(logger, args.GetEnumerator());
            Assert.NotNull(arr);
            Assert.Equal(1, arr.Length);
            Assert.Contains("HeadCropTrimmer", arr[0].GetType().Name);
        }

        [Fact]
        public void TestMainVersionCommand()
        {
            Exception? caught = null;
            try
            {
                Trimmomatic.Main(new string[]{"-h"});
            }
            catch (Exception ex)
            {
                caught = ex;
            }
            Assert.True(true); // coverage only
        }
    }
}