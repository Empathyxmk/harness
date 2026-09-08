using System;
using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Original
{
    public class UtilsTest
    {
        [Fact]
        public void TestRandomStringNegativeLength()
        {
            Assert.Throws<ArgumentException>(() => Utils.RandomString(-1, "abc"));
        }

        [Fact]
        public void TestRandomStringWithEmptyChars()
        {
            Assert.Throws<ArgumentException>(() => Utils.RandomString(5, ""));
        }

        [Fact]
        public void TestRandomStringWithValidInput()
        {
            string result = Utils.RandomString(8, "abcd");
            Assert.NotNull(result);
            Assert.Equal(8, result.Length);
            Assert.Matches("^[abcd]{8}$", result);
        }

        [Fact]
        public void TestGetRandomIntEdgeCases()
        {
            Assert.Equal(5, Utils.GetRandomInt(5, 5));
            Assert.Equal(42, Utils.GetRandomInt(42, 42));
        }

        [Fact]
        public void TestGetRandomIntRange()
        {
            for (int i = 0; i < 100; ++i)
            {
                int result = Utils.GetRandomInt(10, 20);
                Assert.InRange(result, 10, 20);
            }
        }

        [Fact]
        public void TestCreateMapFromPairsEvenArguments()
        {
            var map = Utils.CreateMapFromPairs<string, object>("k1", 123, "k2", "vv", "k3", null);
            Assert.Equal(3, map.Count);
            Assert.Equal(123, map["k1"]);
            Assert.Equal("vv", map["k2"]);
            Assert.Null(map["k3"]);
        }

        [Fact]
        public void TestCreateMapFromPairsOddArguments()
        {
            Assert.Throws<ArgumentException>(() => Utils.CreateMapFromPairs<string, object>("a", "b", "c"));
        }

        [Fact]
        public void TestToHex()
        {
            byte[] b = new byte[] { 0, 10, 15, 16, 31, 127, 255 };
            string hex = Utils.ToHex(b);
            Assert.Matches("^[0-9a-f]{14}$", hex);
            Assert.Equal("000a0f101f7fff", hex);
        }

        [Fact]
        public void TestToHexNull()
        {
            Assert.Null(Utils.ToHex(null));
        }

        [Fact]
        public void TestToHexEmpty()
        {
            Assert.Equal("", Utils.ToHex(new byte[0]));
        }

        [Fact]
        public void TestJoinSimple()
        {
            string[] arr = new string[] { "a", "b", "c" };
            string result = Utils.Join(arr, ":");
            Assert.Equal("a:b:c", result);
        }

        [Fact]
        public void TestJoinNull()
        {
            Assert.Equal("", Utils.Join(null, ","));
        }

        [Fact]
        public void TestJoinEmptyArray()
        {
            Assert.Equal("", Utils.Join(new string[0], "|"));
        }

        [Fact]
        public void TestJoinNoSeparator()
        {
            string[] arr = { "x", "y" };
            Assert.Equal("xy", Utils.Join(arr, ""));
        }
    }
}