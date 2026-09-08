using Xunit;
using ProjectName;
using System;

namespace ProjectName.Tests.Original
{
    public class ChunkedCodingConverterTests
    {
        [Fact]
        public void TestEncode_SimpleString()
        {
            string input = "Hello";
            string expected = "5\r\nHello\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestEncode_EmptyString()
        {
            string input = "";
            string expected = "0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestEncode_LongString()
        {
            string input = "abcdefghijklmnopqrstuvwxyz";
            string expected = "1a\r\nabcdefghijklmnopqrstuvwxyz\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_ValidChunked()
        {
            string input = "5\r\nHello\r\n5\r\nWorld\r\n0\r\n\r\n";
            string expected = "HelloWorld";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_EmptyChunked()
        {
            string input = "0\r\n\r\n";
            string expected = "";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_InvalidHex()
        {
            string input = "GG\r\nInvalid\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestDecode_MissingCRLF_AfterChunkData()
        {
            string input = "5\r\nHello6\r\nWorld!\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestDecode_ChunkWithExtensions()
        {
            string input = "4;xtest\r\nTest\r\n3 ;xfoo\r\nAbc\r\n0\r\n\r\n";
            string expected = "TestAbc";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_ExtraCRLF_BetweenChunks()
        {
            string input = "3\r\nHey\r\n\r\n2\r\nYo\r\n0\r\n\r\n";
            string expected = "HeyYo";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_WithSpacesInChunkExt()
        {
            string input = "5 ;bar=10\r\nApple\r\n4\r\nTest\r\n0\r\n\r\n";
            string expected = "AppleTest";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_WithDifferentChunkSizes()
        {
            string input = "2\r\nAB\r\n3\r\nCDE\r\n1\r\nF\r\n0\r\n\r\n";
            string expected = "ABCDEF";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_NonASCII()
        {
            string input = "6\r\n你好吗\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestEncode_Unicode()
        {
            string input = "你好吗";
            string expected = "9\r\n你好吗\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_CapitalHex()
        {
            string input = "A\r\n1234567890\r\n0\r\n\r\n";
            string expected = "1234567890";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_LowercaseHex()
        {
            string input = "a\r\nabcdefghij\r\n0\r\n\r\n";
            string expected = "abcdefghij";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestEncode_CapitalAndLowercase()
        {
            string input = "AbCdEf";
            string expected = "6\r\nAbCdEf\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_SingleChunk()
        {
            string input = "8\r\n12345678\r\n0\r\n\r\n";
            string expected = "12345678";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestEncode_MultibyteCharacter()
        {
            string input = "ß";
            string expected = "2\r\nß\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_UTF8()
        {
            string input = "2\r\n你好\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestDecode_TrailingCharactersAfterLastChunk()
        {
            string input = "5\r\nHello\r\n0\r\n\r\nabc";
            string expected = "Hello";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }
    }
}