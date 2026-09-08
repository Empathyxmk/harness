using System;
using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Public
{
    public class UtilsExtraPublicTest
    {
        [Fact]
        public void TestRandomStringAllCharsEdgeDifferent()
        {
            // Only one allowed char, different char
            string result = Utils.RandomString(3, "z");
            Assert.Equal("zzz", result);
        }

        [Fact]
        public void TestGetRandomIntMinGreaterThanMaxThrowsDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.GetRandomInt(10, 2));
        }

        [Fact]
        public void TestCreateMapFromPairsTypeSafetyDifferent()
        {
            var m = Utils.CreateMapFromPairs<string, double>("x", 0.1, "y", 2.2);
            Assert.Equal(0.1, m["x"]);
            Assert.Equal(2.2, m["y"]);
        }

        [Fact]
        public void TestToHexUpperByteValuesDifferent()
        {
            byte[] arr = { 0xde, 0xad, 0xbe, 0xef };
            string hex = Utils.ToHex(arr);
            Assert.Equal("deadbeef", hex);
        }

        [Fact]
        public void TestJoinWithOnlyOneElementDifferent()
        {
            string[] arr = { "onlyone" };
            Assert.Equal("onlyone", Utils.Join(arr, ","));
        }
    }
}