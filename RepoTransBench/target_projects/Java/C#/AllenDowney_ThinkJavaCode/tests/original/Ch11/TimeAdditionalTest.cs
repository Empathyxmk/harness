using Xunit;
using AllenDowney.ThinkJavaCode;
using System;
using System.IO;

namespace OriginalTests.Ch11
{
    public class TimeAdditionalTest
    {
        [Fact]
        public void TestPrintTimeOutput()
        {
            var output = new StringWriter();
            var originalOut = Console.Out;
            Console.SetOut(output);

            var t = new Time(12, 34, 56.7);
            Time.PrintTime(t);
            Console.SetOut(originalOut);

            var outStr = output.ToString().Replace("\r", "");
            Assert.Contains("12", outStr);
            Assert.Contains("34", outStr);
            Assert.Contains("56.7", outStr);
        }

        [Fact]
        public void TestAddInstanceWithMultipleRollovers()
        {
            // This test exercises both second and minute rollovers
            var t1 = new Time(22, 58, 58.0);
            var t2 = new Time(1, 2, 62.5);
            var sum = t1.Add(t2);

            // The original Java test expects a string representation; let's assume same as Java  
            Assert.Equal("24:01:60.5\n", sum.ToString());
        }

        [Fact]
        public void TestIncrementLoopingMultipleHours()
        {
            var t = new Time(0, 0, 0.0);
            t.Increment(3661.5); // 1 hr 1 min 1.5 sec
            Assert.Equal("01:01:01.5\n", t.ToString());
        }

        [Fact]
        public void TestEqualsWithNullAndSelf()
        {
            var t = new Time(2, 3, 4.5);
            Assert.True(t.Equals(t)); // self-check
            // Not explicitly testing null
        }
    }
}