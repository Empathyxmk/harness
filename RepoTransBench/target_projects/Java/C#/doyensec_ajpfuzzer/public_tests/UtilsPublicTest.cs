using System;
using Xunit;
using Doyensec.Ajpfuzzer;
using System.Collections.Generic;

namespace Doyensec.Ajpfuzzer.Tests.Public
{
    public class UtilsPublicTest
    {
        [Fact]
        public void TestRandomStringNegativeLengthDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.RandomString(-5, "xyz"));
        }

        [Fact]
        public void TestRandomStringWithEmptyCharsDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.RandomString(3, ""));
        }

        [Fact]
        public void TestRandomStringWithValidDifferentInput()
        {
            string result = Utils.RandomString(6, "wxyz");
            Assert.NotNull(result);
            Assert.Equal(6, result.Length);
            Assert.Matches("^[wxyz]{6}$", result);
        }

        [Fact]
        public void TestGetRandomIntEdgeCasesDifferent()
        {
            Assert.Equal(7, Utils.GetRandomInt(7, 7));
            Assert.Equal(100, Utils.GetRandomInt(100, 100));
        }

        [Fact]
        public void TestGetRandomIntRangeDifferent()
        {
            for (int i = 0; i < 50; ++i)
            {
                int result = Utils.GetRandomInt(20, 30);
                Assert.InRange(result, 20, 30);
            }
        }

        [Fact]
        public void TestCreateMapFromPairsEvenArgumentsDifferent()
        {
            var map = Utils.CreateMapFromPairs<string, object>("key1", 555, "key2", 789, "key3", "value3");
            Assert.Equal(3, map.Count);
            Assert.Equal(555, map["key1"]);
            Assert.Equal(789, map["key2"]);
            Assert.Equal("value3", map["key3"]);
        }

        [Fact]
        public void TestCreateMapFromPairsOddArgumentsDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.CreateMapFromPairs<string, object>("foo", "bar", "baz"));
        }

        [Fact]
        public void TestToHexDifferent()
        {
            byte[] b = new byte[] { 1, 11, 17, 22, 51, 128, 200 };
            string hex = Utils.ToHex(b);
            Assert.Matches("^[0-9a-f]{14}$", hex);
            Assert.Equal("010b11163380c8", hex);
        }

        [Fact]
        public void TestToHexNullDifferent()
        {
            Assert.Null(Utils.ToHex(null));
        }

        [Fact]
        public void TestToHexEmptyDifferent()
        {
            Assert.Equal("", Utils.ToHex(new byte[0]));
        }

        [Fact]
        public void TestJoinSimpleDifferent()
        {
            string[] arr = new string[] { "foo", "bar", "baz" };
            string result = Utils.Join(arr, "-");
            Assert.Equal("foo-bar-baz", result);
        }

        [Fact]
        public void TestJoinNullDifferent()
        {
            Assert.Equal("", Utils.Join(null, "&"));
        }

        [Fact]
        public void TestJoinEmptyArrayDifferent()
        {
            Assert.Equal("", Utils.Join(new string[0], "~"));
        }

        [Fact]
        public void TestJoinNoSeparatorDifferent()
        {
            string[] arr = { "d", "e", "f" };
            Assert.Equal("def", Utils.Join(arr, ""));
        }
    }
}