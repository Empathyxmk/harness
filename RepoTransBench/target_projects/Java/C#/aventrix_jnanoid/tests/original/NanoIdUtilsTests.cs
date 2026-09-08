using System;
using System.Linq;
using System.Reflection;
using Xunit;
using Aventrix.JNanoId;
using System.Security.Cryptography;

namespace Aventrix.JNanoId.Tests.Original
{
    public class NanoIdUtilsTests
    {
        [Fact]
        public void TestDefaultRandomNanoId()
        {
            string nanoid = NanoIdUtils.RandomNanoId();
            Assert.NotNull(nanoid);
            Assert.Equal(NanoIdUtils.DEFAULT_SIZE, nanoid.Length);
            foreach (char c in nanoid)
            {
                Assert.True(NanoIdUtils.DEFAULT_ALPHABET.Contains(c));
            }
        }

        [Fact]
        public void TestRandomNanoIdWithCustomSize()
        {
            int length = 10;
            string nanoid = NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), NanoIdUtils.DEFAULT_ALPHABET, length);
            Assert.NotNull(nanoid);
            Assert.Equal(length, nanoid.Length);
        }

        [Fact]
        public void TestRandomNanoIdWithMinMaxSize()
        {
            int length = 1;
            string nanoid = NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), NanoIdUtils.DEFAULT_ALPHABET, length);
            Assert.Equal(length, nanoid.Length);

            length = 1024;
            nanoid = NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), NanoIdUtils.DEFAULT_ALPHABET, length);
            Assert.Equal(length, nanoid.Length);
        }

        [Fact]
        public void TestRandomNanoIdZeroSize()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), NanoIdUtils.DEFAULT_ALPHABET, 0)
            );
        }

        [Fact]
        public void TestRandomNanoIdNegativeSize()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), NanoIdUtils.DEFAULT_ALPHABET, -1)
            );
        }

        [Fact]
        public void TestRandomNanoIdNullRandom()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId((RandomNumberGenerator)null, NanoIdUtils.DEFAULT_ALPHABET, 10)
            );
        }

        [Fact]
        public void TestRandomNanoIdNullAlphabet()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), null, 10)
            );
        }

        [Fact]
        public void TestRandomNanoIdEmptyAlphabet()
        {
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), new char[0], 10)
            );
        }

        [Fact]
        public void TestRandomNanoIdOversizedAlphabet()
        {
            char[] bigAlphabet = new char[256];
            for (int i = 0; i < bigAlphabet.Length; i++)
            {
                bigAlphabet[i] = (char)('a' + (i % 26));
            }
            Assert.Throws<ArgumentException>(() =>
                NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), bigAlphabet, 10)
            );
        }

        [Fact]
        public void TestNanoIdIsUrlFriendly()
        {
            string nanoid = NanoIdUtils.RandomNanoId();
            Assert.Matches(@"^[_\-0-9a-zA-Z]+$", nanoid);
        }

        [Fact]
        public void TestNanoIdUtilsPrivateConstructor()
        {
            // For code coverage, ensure NanoIdUtils has no accessible constructor
            var ctors = typeof(NanoIdUtils).GetConstructors(BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
            foreach (var ctor in ctors)
            {
                Assert.True(ctor.IsPrivate || ctor.IsStatic);
            }
        }

        [Fact]
        public void TestRandomNanoIdWithNonDefaultRandom()
        {
            var rng = new Random(1234);
            char[] alpha = NanoIdUtils.DEFAULT_ALPHABET;
            int len = 11;
            string nanoid = NanoIdUtils.RandomNanoId(rng, alpha, len);
            Assert.NotNull(nanoid);
            Assert.Equal(len, nanoid.Length);
        }

        [Fact]
        public void TestRandomNanoIdWithSmallAlphabet()
        {
            char[] alphabet = { 'a', 'b' };
            string nanoid = NanoIdUtils.RandomNanoId(RandomNumberGenerator.Create(), alphabet, 6);
            Assert.Equal(6, nanoid.Length);
            foreach (char c in nanoid)
            {
                Assert.True(c == 'a' || c == 'b');
            }
        }

        [Fact]
        public void TestNanoIdUniqueness()
        {
            string nanoid1 = NanoIdUtils.RandomNanoId();
            string nanoid2 = NanoIdUtils.RandomNanoId();
            Assert.NotEqual(nanoid1, nanoid2);
        }
    }
}