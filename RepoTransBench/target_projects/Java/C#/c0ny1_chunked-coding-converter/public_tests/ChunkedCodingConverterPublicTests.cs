using Xunit;
using ProjectName;
using System;

namespace ProjectName.Tests.Public
{
    public class ChunkedCodingConverterPublicTests
    {
        [Fact]
        public void TestEncode_SimpleString()
        {
            string input = "Earth";
            string expected = "5\r\nEarth\r\n0\r\n\r\n";
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
            string input = "pqrstuvwxyz";
            string expected = "b\r\npqrstuvwxyz\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_ValidChunked()
        {
            string input = "4\r\nCode\r\n3\r\nGen\r\n0\r\n\r\n";
            string expected = "CodeGen";
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
            string input = "QR\r\nfail\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestDecode_MissingCRLF_AfterChunkData()
        {
            string input = "6\r\nplanet5\r\nEarth\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestDecode_ChunkWithExtensions()
        {
            string input = "2;xy\r\nHi\r\n3;test\r\nSun\r\n0\r\n\r\n";
            string expected = "HiSun";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_ExtraCRLF_BetweenChunks()
        {
            string input = "1\r\ne\r\n\r\n2\r\nok\r\n0\r\n\r\n";
            string expected = "eok";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_WithSpacesInChunkExt()
        {
            string input = "4 ;a\r\nJava\r\n5\r\nTests\r\n0\r\n\r\n";
            string expected = "JavaTests";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_WithDifferentChunkSizes()
        {
            string input = "3\r\nbye\r\n1\r\n!\r\n2\r\nok\r\n0\r\n\r\n";
            string expected = "bye!ok";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_NonASCII()
        {
            string input = "2\r\nαβ\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestEncode_Unicode()
        {
            string input = "测试";
            string expected = "6\r\n测试\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_CapitalHex()
        {
            string input = "B\r\n12345678901\r\n0\r\n\r\n";
            string expected = "12345678901";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_LowercaseHex()
        {
            string input = "9\r\nchunkdata\r\n0\r\n\r\n";
            string expected = "chunkdata";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestEncode_CapitalAndLowercase()
        {
            string input = "GenAI";
            string expected = "5\r\nGenAI\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_SingleChunk()
        {
            string input = "4\r\nabcd\r\n0\r\n\r\n";
            string expected = "abcd";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestEncode_MultibyteCharacter()
        {
            string input = "ø";
            string expected = "2\r\nø\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Encode(input);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestDecode_UTF8()
        {
            string input = "2\r\nλμ\r\n0\r\n\r\n";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }

        [Fact]
        public void TestDecode_TrailingCharactersAfterLastChunk()
        {
            string input = "3\r\nxyz\r\n0\r\n\ntail";
            string result = ChunkedCodingConverter.Decode(input);
            Assert.Null(result);
        }
    }
}