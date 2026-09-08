using System;
using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Original
{
    public class UtilsExtraTest
    {
        [Fact]
        public void TestRandomStringAllCharsEdge()
        {
            // Only one allowed char, should repeat
            string result = Utils.RandomString(5, "x");
            Assert.Equal("xxxxx", result);
        }

        [Fact]
        public void TestGetRandomIntMinGreaterThanMaxThrows()
        {
            Assert.Throws<ArgumentException>(() => Utils.GetRandomInt(5, 2));
        }

        [Fact]
        public void TestCreateMapFromPairsTypeSafety()
        {
            var m = Utils.CreateMapFromPairs<int, string>(1, "a", 2, "b");
            Assert.Equal("a", m[1]);
            Assert.Equal("b", m[2]);
        }

        [Fact]
        public void TestToHexUpperByteValues()
        {
            byte[] arr = { 0xaf, 0xff, 0xb4 };
            string hex = Utils.ToHex(arr);
            Assert.Equal("afffb4", hex);
        }

        [Fact]
        public void TestJoinWithOnlyOneElement()
        {
            string[] arr = { "solo" };
            Assert.Equal("solo", Utils.Join(arr, ","));
        }
    }
}