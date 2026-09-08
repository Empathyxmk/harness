using System;
using System.Linq;
using Xunit;
using Aventrix.JNanoId;
using System.Security.Cryptography;

namespace Aventrix.JNanoId.Tests.Public
{
    public class NanoIdUtilsPublicTests
    {
        private string CharArrayToString(char[] arr)
        {
            return new string(arr);
        }

        [Fact]
        public void Test_randomNanoId_noArgs_lengthAndAlphabet()
        {
            string nanoid = NanoIdUtils.RandomNanoId();
            Assert.NotNull(nanoid);
            Assert.Equal(21, nanoid.Length);

            string defaultAlphabetStr = CharArrayToString(NanoIdUtils.DEFAULT_ALPHABET);
            foreach (char c in nanoid)
            {
                Assert.Contains(c.ToString(), defaultAlphabetStr);
            }
        }

        [Fact]
        public void Test_randomNanoId_customAlphabet_public()
        {
            char[] customAlphabet = { 'a', 'B', '4', '!' };
            int size = 13;
            string nanoid = NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), customAlphabet, size);
            Assert.NotNull(nanoid);
            Assert.Equal(size, nanoid.Length);
            string alphaStr = CharArrayToString(customAlphabet);
            foreach (char c in nanoid)
            {
                Assert.Contains(c.ToString(), alphaStr);
            }
        }

        [Fact]
        public void Test_randomNanoId_nullAlphabet_public()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), null, 10)
            );
        }

        [Fact]
        public void Test_randomNanoId_emptyAlphabet_public()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), new char[0], 8)
            );
        }

        [Fact]
        public void Test_randomNanoId_tooShortLength_public()
        {
            char[] alphabet = { 'a', 'b' };
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), alphabet, 0)
            );
        }

        [Fact]
        public void Test_randomNanoId_negativeLength_public()
        {
            char[] alphabet = { 'a', 'b', 'c' };
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), alphabet, -5)
            );
        }

        [Fact]
        public void Test_randomNanoId_alphabetTooLong_public()
        {
            char[] alphabet = new char[300];
            for (int i = 0; i < 300; i++)
            {
                alphabet[i] = (char)(32 + (i % 94));
            }
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), alphabet, 8)
            );
        }

        [Fact]
        public void Test_randomNanoId_customRandom_public()
        {
            var predictableRandom = new Random(42L.GetHashCode()); // C# Random constructor uses int seed
            char[] alphabet = { 'Q', 'W', 'E' };
            int size = 6;
            string nanoid = NanoIdUtils.RandomNanoId(predictableRandom, alphabet, size);
            Assert.Equal(size, nanoid.Length);
            string alphabetString = CharArrayToString(alphabet);
            foreach (char c in nanoid)
            {
                Assert.Contains(c.ToString(), alphabetString);
            }
            // Deterministic value for this random+alphabet combination
            string expected = NanoIdUtils.RandomNanoId(new Random(42L.GetHashCode()), alphabet, size);
            Assert.Equal(expected, nanoid);
        }

        [Fact]
        public void Test_randomNanoId_defaultRandom_public()
        {
            int length = 17;
            char[] defaultAlphabet = NanoIdUtils.DEFAULT_ALPHABET;
            string nanoid = NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), defaultAlphabet, length);
            Assert.Equal(length, nanoid.Length);
            string defaultAlphabetStr = CharArrayToString(defaultAlphabet);
            foreach (char c in nanoid)
            {
                Assert.Contains(c.ToString(), defaultAlphabetStr);
            }
        }
    }
}